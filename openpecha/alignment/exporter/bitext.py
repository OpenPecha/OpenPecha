from pathlib import Path

from openpecha.alignment.exporter import Exporter


class BitextExporter(Exporter):
    def serialize_segment_pair(self, pair_id, segment_pair, segment_texts):
        segment_pair_text = ""
        for pair_c, (pecha_id, segment_id) in enumerate(segment_pair.items(), 1):
            segment_text = segment_texts[pecha_id][pair_id]
            segment_text = segment_text.replace("\n", "")
            if pair_c == 1:
                segment_pair_text += f"{segment_text}\n"
            else:
                segment_pair_text += f"\t{segment_text}\n"
        return segment_pair_text

    def export(self, output_file_path):
        bi_text = ""
        segment_srcs = self.alignment.get("segment_sources", {})
        segment_texts = {}
        for seg_src_id, seg_src in segment_srcs.items():
            segment_texts[seg_src_id] = self.get_segment_texts(seg_src_id)
        for pair_id, segment_pair in self.alignment.get("segment_pairs", {}):
            bi_text += self.serialize_segment_pair(pair_id, segment_pair, segment_texts)
        Path(output_file_path).write_text(bi_text, encoding="utf-8")
