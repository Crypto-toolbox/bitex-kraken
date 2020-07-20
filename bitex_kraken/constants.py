EXCHANGE_NAME = "kraken"
API_BASE_URL = "https://api.kraken"
API_VERSION = "0"
VERSIONED_API_URL = f"{API_BASE_URL}/{API_VERSION}"

PUBLIC_ENDPOINTS = ["Depth", "Trades", "OHLC", "Ticker", "AssetPairs", "Assets", "Time", "Spread"]
ENDPOINT_MAPPING = {
    # Public Endpoints
    "book": "Depth",
    "pairs": "AssetPairs",
    "trades": "Trades",
    "ticker": "Ticker",

    # Private Endpoints
    "order": {
        "cancel": "CancelOrder",
        "new": "AddOrder",
        "status": "QueryOrders",
    },

    "wallet": {
        "deposit": "DepositAddresses",
        "withdraw": "Withdraw",
    }
}