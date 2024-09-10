from uuid import UUID

from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import AssetClass, OrderSide, QueryOrderStatus, TimeInForce
from alpaca.trading.requests import GetAssetsRequest, GetOrdersRequest, LimitOrderRequest, MarketOrderRequest
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import status


class AlpacaIntegrationAccount:
    """Alpaca integration."""

    restricted_message = "Account is currently restricted from trading."

    def __init__(self):
        self.trading_client = TradingClient(
            settings.API_KEY_ALPACA,
            settings.SECRET_KEY_ALPACA,
        )

    def get_account_info(self):
        """Get account info."""
        account = self.trading_client.get_account()
        if account.trading_blocked:
            raise ValidationError(
                self.restricted_message,
                params={"status": status.HTTP_403_FORBIDDEN},
            )
        # Check how much money we can use to open new positions.
        # print('${} is available as buying power.'.format(account.buying_power))

        return account

    def get_view_gain_loss_portfolio(self):
        """Get view gain loss portfolio."""
        account = self.trading_client.get_account()
        if account.trading_blocked:
            raise ValidationError(
                self.restricted_message,
                params={"status": status.HTTP_403_FORBIDDEN},
            )
        balance_change = float(account.equity) - float(account.last_equity)
        return balance_change


class AlpacaIntegrationDataHistorical:
    """Alpaca integration data."""

    def __init__(self):
        self.client = CryptoHistoricalDataClient()
        # TODO: update to use request_params to filter data
        self.request_params = CryptoBarsRequest(
            symbol_or_symbols=["BTC/USD", "ETH/USD"],
            timeframe=TimeFrame.Day,
            start="2024-02-13",
        )

    def get_crypto_bars(self):
        """Get crypto bars."""

        bars = self.client.get_crypto_bars(self.request_params)
        return bars

    def get_crypto_trades(self):
        """Get crypto trades."""

        trades = self.client.get_crypto_trades(self.request_params)
        return trades

    def get_crypto_latest_bar(self):
        """Get crypto quotes."""

        quotes = self.client.get_crypto_latest_bar(self.request_params)
        return quotes

    def get_crypto_latest_quote(self):
        """Get crypto quotes."""

        quotes = self.client.get_crypto_latest_quote(self.request_params)
        return quotes

    def get_crypto_latest_trade(self):
        """Get crypto quotes."""

        quotes = self.client.get_crypto_latest_trade(self.request_params)
        return quotes

    def get_crypto_snapshot(self):
        """Get crypto quotes."""

        quotes = self.client.get_crypto_snapshot(self.request_params)
        return quotes


class AlpacaIntegrationAssets:
    """Alpaca integration assets."""

    def __init__(self):
        self.trading_client = TradingClient(
            settings.API_KEY_ALPACA,
            settings.SECRET_KEY_ALPACA,
        )

    def get_assets(self):
        """Get assets."""
        # TODO: update to use request_params to search for any equities
        # search for US equities
        search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)

        return search_params

    def get_asset(self, symbol):
        """Get asset."""
        asset = self.trading_client.get_asset(symbol)
        return asset

    def add_asset_to_watchlist_by_id(self, asset_id):
        """Get asset by id."""
        asset = self.trading_client.add_asset_to_watchlist_by_id(asset_id)
        return asset

    def remove_asset_from_watchlist_by_id(self, asset_id):
        """Remove asset from watchlist."""
        asset = self.trading_client.remove_asset_from_watchlist_by_id(asset_id)
        return asset

    def get_watchlists(self):
        """Get watchlist."""
        watchlist = self.trading_client.get_watchlists()
        return watchlist

    def get_watchlist_by_id(self, watchlist_id):
        """Get watchlist by id."""
        watchlist = self.trading_client.get_watchlist_by_id(watchlist_id)
        return watchlist

    def create_watchlist(self, name):
        """Create watchlist."""
        watchlist = self.trading_client.create_watchlist(name)
        return watchlist

    def delete_watchlist_by_id(self, watchlist_id):
        """Delete watchlist by id."""
        watchlist = self.trading_client.delete_watchlist_by_id(watchlist_id)
        return watchlist

    def update_watchlist_by_id(self, watchlist_id, name):
        """Update watchlist by id."""
        watchlist = self.trading_client.update_watchlist_by_id(watchlist_id, name)
        return watchlist


class AlpacaIntegrationOrders:
    """Alpaca integration orders."""

    def __init__(self):
        self.trading_client = TradingClient(
            settings.API_KEY_ALPACA,
            settings.SECRET_KEY_ALPACA,
            paper=True,  # use paper trading environment
        )

    def get_orders(self):
        """Get orders."""
        # TODO: update to use request_params to filter orders
        get_orders_data = GetOrdersRequest(
            status=QueryOrderStatus.CLOSED,
            limit=100,
            nested=True,  # show nested multi-leg orders
        )
        orders = self.trading_client.get_orders(filter=get_orders_data)
        return orders

    def get_order(self, order_id: UUID):
        """Get order."""
        order = self.trading_client.get_order_by_id(order_id)
        return order

    def place_order(
        self,
        request_data,
    ):
        """Place order."""
        # preparing market order
        market_order_data = MarketOrderRequest(
            symbol=str(request_data["symbol"]).upper(),
            qty=float(request_data["qty"]),
            side=request_data["side"],
            time_in_force=request_data["time_in_force"],
        )

        # Market order
        market_order = self.trading_client.submit_order(order_data=market_order_data)  # noqa

        return market_order

    def place_limit_order_data(
        self,
        request_data,
    ):
        """Place limit order."""
        # preparing limit order
        limit_order_data = LimitOrderRequest(
            symbol=str(request_data["symbol"]).upper(),
            limit_price=request_data["limit_price"],
            notional=request_data["notional"],
            side=request_data["side"],
            time_in_force=request_data["time_in_force"],
        )

        # Limit order
        limit_order = self.trading_client.submit_order(order_data=limit_order_data)

        return limit_order

    def cancel_order(self, order_id: UUID):
        """Cancel order."""
        order = self.trading_client.cancel_order_by_id(order_id)
        return order

    def cancel_all_orders(self):
        """Cancel all orders."""
        orders = self.trading_client.cancel_orders()
        return orders

    def submit_shortsale(self):
        """Submit short sale."""
        market_order_data = MarketOrderRequest(symbol="SPY", qty=1, side=OrderSide.SELL, time_in_force=TimeInForce.GTC)

        # Market order
        market_order = self.trading_client.submit_order(order_data=market_order_data)

        return market_order


class AlpacaIntegrationPositions:
    """Alpaca integration positions."""

    def __init__(self):
        self.trading_client = TradingClient(
            settings.API_KEY_ALPACA,
            settings.SECRET_KEY_ALPACA,
        )

    def get_positions(self):
        """Get positions."""
        positions = self.trading_client.get_all_positions()
        # # Print the quantity of shares for each position.
        # for position in portfolio:
        #     print("{} shares of {}".format(position.qty, position.symbol))
        return positions

    def close_position(self, symbol):
        """Close position."""
        position = self.trading_client.close_position(symbol)
        return position

    def close_all_positions(self):
        """Close all positions."""
        positions = self.trading_client.close_all_positions()
        return positions
