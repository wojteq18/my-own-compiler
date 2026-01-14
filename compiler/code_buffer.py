class CodeBuffer: 
    def __init__(self):
        self.instructions = []
        self.labels = {}
        self.label_counter = 0

    def get_new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def add_instr(self, instr):
        self.instructions.append(instr)

    def set_label(self, label_name):
        self.labels[label_name] = len(self.instructions)

    def finalize(self):
        final_output = []
        sorted_labels = sorted(self.labels.items(), key=lambda x: len(x[0]), reverse=True)
        for instr in self.instructions:
            processed_instr = instr
            for label, line_num in sorted_labels:
                placeholder = f"LABEL_{label}"
                if placeholder in processed_instr:
                    processed_instr = processed_instr.replace(placeholder, str(line_num))    

            final_output.append(processed_instr)
        return "\n".join(final_output)