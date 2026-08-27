from app.retrieval.retrieval_result import RetrievedChunk


class ContextBuilder:

    def build(
        self,
        chunks: list[RetrievedChunk],
    ) -> str:

        if not chunks:
            return ""

        sections = []

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):
            source = chunk.metadata.get(
                "file_name",
                chunk.metadata.get(
                    "source",
                    chunk.metadata.get(
                        "file_path",
                        "unknown",
                    ),
                ),
            )

            chunk_index = chunk.metadata.get(
                "chunk_index",
                index - 1,
            )

            sections.append(
                "\n".join(
                    [
                        f"SOURCE: {source}",
                        f"CHUNK: {chunk_index}",
                        "",
                        chunk.content,
                    ]
                )
            )

        return "\n\n---\n\n".join(
            sections
        )