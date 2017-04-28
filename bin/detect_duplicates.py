# Helper function to remove duplicate targets
# Input: targets.result() (list of target items)
# Output:


def detect_duplicates(targets):
    ref_tgt = targets[0]
    dup_stack = []
    for target in targets:
        if target.id != ref_tgt.id:
            if (target.shape == ref_tgt.shape) & (target.alphanumeric == ref_tgt.alphanumeric):
                dup_stack.append(target.id)
    return dup_stack
