import json

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


def lambda_handler(event, context):

    n = int(event.get("n", 100))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "n": n,
            "primes": generate_primes(n)
        })
    }


if __name__ == "__main__":

    event = {
        "n": 20
    }

    print(lambda_handler(event, None))
