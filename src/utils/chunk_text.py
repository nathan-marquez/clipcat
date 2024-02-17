def chunk_text(transcript):
    chunk = 0
    wordCount = 0
    text = ""
    chunkDict = {}

    words = transcript.split(' ')

    for word in words:
        # Check if adding the next word would exceed the 100-word limit
        if wordCount < 100:
            # Add a space before the word if it's not the first word in the chunk
            if text:
                text += " "
            text += word
            wordCount += 1
        else:
            # Save the current chunk and start a new one
            chunkDict[chunk] = text
            text = word  # Start the new chunk with the current word
            wordCount = 1  # Reset word count for the new chunk
            chunk += 1

    # After the loop, add the last chunk if it has any text
    if text:
        chunkDict[chunk] = text

    return chunkDict

# Example usage
# transcript = "This is a test transcript. " * 50  # Example transcript with repeated phrase
# chunked_transcript = chunk_text(transcript)

# for key, value in chunked_transcript.items():
#     print(f"Chunk {key}: Word Count = {len(value.split(' '))}")
#     print(value + "\n")
