from reachly_engine.scraping.cleaner import clean_html, aggressive_cleanup


def test_html_cleaning():
    html = """
    <html>
        <head><title>Test</title></head>
        <body>
            <script>alert("x")</script>
            <h1>Hello</h1>
            <p>This is a test</p>
        </body>
    </html>
    """

    text = clean_html(html)
    text = aggressive_cleanup(text)

    assert "Hello" in text
    assert "This is a test" in text
    assert "alert" not in text

