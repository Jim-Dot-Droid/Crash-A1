from solana.rpc.api import Client
from solana.publickey import PublicKey

PROGRAM_ID = PublicKey("DEALERKFspSo5RoXNnKAhRPhTcvJeqeEgAgZsNSjCx5E")
RPC_URLS = [
    "https://api.mainnet-beta.solana.com",
    "https://solana-mainnet.g.alchemy.com/v2/demo"
]

def fetch_latest_multipliers(limit=50):
    for url in RPC_URLS:
        try:
            client = Client(url)
            sigs = client.get_signatures_for_address(PROGRAM_ID, limit=limit)['result']
            rounds = []
            for sig in sigs:
                tx = client.get_transaction(sig['signature'])['result']
                logs = tx['meta']['logMessages']
                for log in logs:
                    if "multiplier" in log:
                        try:
                            val = float(log.split()[-1].replace('x', ''))
                            rounds.append(val)
                        except:
                            continue
            if rounds:
                return rounds
        except:
            continue
    return []