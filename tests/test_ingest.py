from app.ingest import chunk_text

def test_chunk_text_basic():
    """Test that chunk_text returns a list of non-empty strings."""
    text = "Paragraph one.\n\nParagraph two.\n\nParagraph three."
    chunks = chunk_text(text, chunk_size=30, overlap=5)
    
    assert isinstance(chunks, list)
    assert len(chunks) > 0
    assert all(isinstance(c, str) for c in chunks)
    assert all(len(c) > 0 for c in chunks)

def test_chunk_text_empty():
    """Test that chunk_text handles empty input gracefully."""
    chunks = chunk_text("")
    assert chunks == []