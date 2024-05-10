# This code was inspired by this example
# https://www.linkedin.com/posts/hanane-d-algo-trader_react-financial-agent-llamaindex-activity-7186333474256035840-jyQV/?utm_source=share&utm_medium=member_desktop
# I modified it with the intention of trying new ideas and improving it for my own needs

from llama_index.core.tools.tool_spec.base import BaseToolSpec
from llama_index.llms.openai import OpenAI
from llama_index.core.readers.base import Document
from newsapi import NewsApiClient
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, datetime
from typing import Optional
import os


LLM = OpenAI("gpt-4")
NEWS_API_CLIENT = NewsApiClient(os.environ["NEWS_API_KEY"])


class FinanceTools(BaseToolSpec):
    """
    A class for various financial tools, leveraging external APIs to
        fetch stock data and news articles.
    """

    spec_functions = [
        "stock_prices",
        "plot_stock_price",
        "search_news",
        "summarize_news",
    ]

    def stock_prices(
        self, ticker: str, period_days: Optional[int] = 1
    ) -> pd.DataFrame:
        """Retrieves stock information for the given period of days.

        Args:
            ticker (str): The stock ticker.
            period_days (int, optional): Period of days to retrieve. Defaults to 1.

        Returns:
            pd.DataFrame: DataFrame containing stock's prices.
        """
        stock = yf.Ticker(ticker)
        df = stock.history(period=f"{period_days}d")
        return df

    def plot_stock_price(
        self,
        ticker: str,
        period_days: int,
        info_names: Optional[list] = ["Close"],
    ) -> bool:
        """Plots selected stock data for the last month for a given ticker.

        Args:
            ticker (str): The stock ticker.
            period_days (int): Period of days to plot
            info_names (list, optional): List of columns to plot. Defaults to ["Close"].

        Returns:
            bool: Bool telling if function succeeded or not.
        """
        try:
            df = self.stock_prices(ticker, period_days)
            df[info_names].plot(title=f"{ticker} Historical Data")
            plt.xlabel("Date")
            plt.ylabel("Values")
            plt.show()
            return True
        except:
            return False

    def search_news(
        self,
        ticker: str,
        num_articles: Optional[int] = 3,
        from_date: Optional[str] = str(date.today()),
        to_date: Optional[str] = str(date.today()),
    ) -> str:
        """Searches for recent news articles related to a given stock ticker.

        Args:
            ticker (str): The stock ticker.
            num_articles (int, optional): Number of news articles to retrieve.
                Defaults to 3.
            from_date (str, optional): Start date (format: %Y-%m-%d) of news articles.
                Defaults to today's date.
            to_date (str, optional): End date (format: %Y-%m-%d) of news articles.
                Defaults to today's date.

        Returns:
            str: Concatenated string of news titles, descriptions, and partial contents.
        """
        articles = NEWS_API_CLIENT.get_everything(
            q=ticker,
            from_param=datetime.strptime(from_date, "%Y-%m-%d").isoformat(),
            to=datetime.strptime(to_date, "%Y-%m-%d").isoformat(),
            language="en",
            sort_by="relevancy",
            page_size=num_articles,
        )

        news_concat = [
            f"""    ```````
            Article #{a}
            Title: {article['title']}
            Description: {article['description']}
            Content: {article['content'][:500]}
            """
            for a, article in enumerate(articles["articles"])
        ]

        # This may be a large response so storing it a indices
        return [Document(text=".\n".join(news_concat))]

    def summarize_news(
        self,
        ticker: str,
        num_articles: Optional[int] = 3,
        from_date: Optional[str] = str(date.today()),
        to_date: Optional[str] = str(date.today()),
    ) -> str:
        """Generates a summary for the latest news related to a specific ticker.

        Args:
            ticker (str): The stock ticker.
            num_articles (int, optional): Number of news articles to retrieve.
                Defaults to 3.
            from_date (str, optional): Start date (format: %Y-%m-%d) of news articles.
                Defaults to today's date.
            to_date (str, optional): End date (format: %Y-%m-%d) of news articles.
                Defaults to today's date.

        Returns:
            str: Summary of the news.
        """
        news = self.search_news(ticker, num_articles, from_date, to_date)
        prompt = (
            f"Summarize the following text by extracting key insights: {news}"
        )
        response = LLM.complete(prompt)

        return str(response)
