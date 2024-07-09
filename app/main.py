from flask import Flask, request, jsonify

from app.src.domain.dto.event_dto import EventDTO
from app.src.domain.entity.account_entity import EventManager
from app.src.domain.exception.event_exception import AccountNotFound, InsufficientFunds, OriginIsRequired
from app.src.infrastructure.config import Config
from app.src.infrastructure.form_request.validate_request import event_validator

app = Flask(__name__)
app.config.from_object(Config())

event_manager = EventManager()


@app.route('/event', methods=['POST'])
def event():
    account: EventDTO
    if not request.is_json:
        return jsonify({"error": "Invalid input"}), 400

    try:
        data = request.get_json()
        event_validator(data)
        event_dto = EventDTO(
            type=data['type'],
            destination=data['destination'],
            amount=data['amount'],
            origin=data['origin'] if 'origin' in data else None
        )

        match event_dto.type:
            case 'deposit':
                account = event_manager.deposit(event_dto)
            case 'withdraw':
                account = event_manager.withdraw(event_dto)
            case 'transfer':
                if not event_dto.origin:
                    raise OriginIsRequired
                origin, destination = event_manager.transfer(event_dto)
                return jsonify({
                    "origin": {"id": origin['account'], "balance": origin['balance']},
                    "destination": {"id": destination['account'], "balance": destination['balance']}}), 201
    except AccountNotFound:
        return jsonify(0), 400
    except InsufficientFunds as i:
        return jsonify({"error": i.msg, "current_fund": i.amount}), 400
    except OriginIsRequired as i:
        return jsonify({"error": i.msg}), 400
    except Exception as e:
        app.logger.error(f"Error processing event.json: {e}")
        return jsonify({"error": str(e)}), 400

    return jsonify({"destination": {"id": account.destination, "balance": account.amount}}), 201


@app.route('/reset', methods=['POST'])
def reset():
    event_manager.reset_events()
    return jsonify('OK'), 200


@app.route('/balance', methods=['GET'])
def balance():
    try:
        account_id = request.args.get('account_id')
        if not account_id:
            return jsonify({"error": "account_id is required"}), 400

        account_balance = event_manager.get_balance(account_id)
    except AccountNotFound:
        return jsonify(), 404
    return jsonify(account_balance), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
