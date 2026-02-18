import json
import logging
import decimalencoder
import todoList

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def _to_bool(value):
        if isinstance(value, bool):
                    return value
                    if isinstance(value, str):
                                return value.strip().lower() in ("true", "1", "yes", "y")
                                return False

                            def update(event, context):
                                    try:
                                                body = event.get("body") or "{}"
                                                        data = json.loads(body) if isinstance(body, str) else body

                                                                todo_id = (event.get("pathParameters") or {}).get("id")
                                                                        if not todo_id:
                                                                                        return {"statusCode": 400, "body": json.dumps({"message": "Missing path parameter id"})}

                                                                                            if "text" not in data or "checked" not in data:
                                                                                                            return {"statusCode": 400, "body": json.dumps({"message": "Validation Failed: text and checked are required"})}

                                                                                                                checked = _to_bool(data["checked"])

                                                                                                                        result = todoList.update_item(todo_id, data["text"], checked)

                                                                                                                                return {
                                                                                                                                                    "statusCode": 200,
                                                                                                                                                                "body": json.dumps(result, cls=decimalencoder.DecimalEncoder)
                                                                                                                                                                        }

                                                                                                                                    except Exception as e:
                                                                                                                                                # Si no puedes ver logs por permisos, al menos devolvemos un body útil
                                                                                                                                                        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

