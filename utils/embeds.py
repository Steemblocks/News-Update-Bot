"""
Discord Embed utilities for formatting news articles
"""
import discord
from datetime import datetime
from typing import List
from news_sources.fetcher import NewsArticle

def create_article_embed(article: NewsArticle) -> discord.Embed:
    """Create a Discord embed from a news article"""
    embed = discord.Embed(
        title=article.title[:256],  # Discord limit
        url=article.url,
        description=article.description[:4096] if article.description else "No description available",
        color=discord.Color.blue()
    )
    
    embed.set_author(name=article.source)
    
    if article.image_url:
        embed.set_image(url=article.image_url)
    
    if article.published:
        embed.add_field(name="Published", value=article.published, inline=False)
    
    embed.timestamp = datetime.now()
    
    return embed

def create_news_summary_embed(region: str, articles: List[NewsArticle], limit: int = 5) -> List[discord.Embed]:
    """Create multiple embeds for a news summary"""
    embeds = []
    
    # Main header embed
    header_embed = discord.Embed(
        title=f"📰 Latest News from {region.upper()}",
        description=f"Top {min(limit, len(articles))} news stories",
        color=discord.Color.gold()
    )
    header_embed.timestamp = datetime.now()
    embeds.append(header_embed)
    
    # Article embeds
    for i, article in enumerate(articles[:limit], 1):
        embed = create_article_embed(article)
        embed.set_footer(text=f"Story {i} of {min(limit, len(articles))}")
        embeds.append(embed)
    
    return embeds

def create_help_embed() -> discord.Embed:
    """Create a help embed with available commands"""
    embed = discord.Embed(
        title="📰 News Bot Help",
        description="Available commands for the News Bot",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="!news usa",
        value="Get latest news from USA",
        inline=False
    )
    embed.add_field(
        name="!news uk",
        value="Get latest news from UK",
        inline=False
    )
    embed.add_field(
        name="!news europe",
        value="Get latest news from Europe",
        inline=False
    )
    embed.add_field(
        name="!news all",
        value="Get latest news from all regions",
        inline=False
    )
    embed.add_field(
        name="!help",
        value="Show this help message",
        inline=False
    )
    embed.timestamp = datetime.now()
    
    return embed
