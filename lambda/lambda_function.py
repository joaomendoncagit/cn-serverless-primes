import json
import time


def generate_primes(n):
    primes = []

    for candidate in range(2, n):
        is_prime = True

        for divisor in range(2, int(candidate**0.5) + 1):
            if candidate % divisor == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(candidate)

    return primes


def get_n_from_event(event):
    if "n" in event:
        return int(event["n"])

    query = event.get("queryStringParameters") or {}
    if "n" in query:
        return int(query["n"])

    body = event.get("body")
    if body:
        if event.get("isBase64Encoded"):
            raise ValueError("Base64 body is not supported")

        data = json.loads(body)
        return int(data.get("n", 100))

    return 100


def lambda_handler(event, context):
    start = time.perf_counter()

    try:
        n = get_n_from_event(event)

        if n < 2:
            raise ValueError("n must be >= 2")

        if n > 100000:
            raise ValueError("n must be <= 100000")

        primes = generate_primes(n)

        duration_ms = (time.perf_counter() - start) * 1000

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "n": n,
                "prime_count": len(primes),
                "primes": primes,
                "execution_time_ms": round(duration_ms, 3)
            })
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }


if __name__ == "__main__":
    print(lambda_handler({"n": 20}, None))