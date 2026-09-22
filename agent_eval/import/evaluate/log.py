def print_metrics(name, metrics, result=None, file=None):

    def output(text=""):
        print(text)

        if file is not None:
            print(text, file=file)

    output("\n" + "=" * 80)
    output(name)
    output("=" * 80)

    output("\n--- COUNTS ---")
    output(f"GT paragraphs:           {metrics['total_gt']}")
    output(f"Predicted sentences:     {metrics['predicted_total']}")
    output(f"Matched predictions:     {metrics['matched_predictions']}")
    output(f"Correct predictions:     {metrics['correct']}")
    output(f"Misclassified:           {metrics['misclassified']}")
    output(f"Extra/unmatched:         {metrics['extra']}")
    output(f"Missing GT:              {metrics['missing_gt']}")

    output("\n--- RATES ---")
    output(f"Sentence match rate:     {metrics['sentence_match_rate']:.2%}")
    output(f"Classification accuracy: {metrics['classification_accuracy']:.2%}")
    output(f"Correct prediction rate: {metrics['correct_prediction_rate']:.2%}")
    output(f"GT recall:               {metrics['gt_recall']:.2%}")
    output(f"Extra sentence rate:     {metrics['extra_rate']:.2%}")
    
    
    
    output("\n--- FIELD MISMATCHES ---")

    mismatches = [
        (key, count)
        for key, count in metrics["confusion_matrix"].items()
        if " -> " in key
        and key.split(" -> ")[0] != key.split(" -> ")[1]
    ]

    if not mismatches:
        output("No field mismatches.")
    else:
        output(
            f"{'GT field':40} "
            f"{'Predicted field':40} "
            f"{'Count':>8}"
        )

        output("-" * 90)

        for key, count in sorted(
            mismatches,
            key=lambda x: x[1],
            reverse=True,
        ):
            gt_field, pred_field = key.split(" -> ", 1)

            output(
                f"{gt_field:40} "
                f"{pred_field:40} "
                f"{count:8}"
            )

    if result is None:
        return

    output("\n--- MISCLASSIFIED PREDICTIONS ---")

    for m in result["matches"]:
        if m["status"] != "misclassified":
            continue

        output("-" * 80)
        output(f"Similarity:      {m['similarity']}")
        output(f"Predicted field: {m['pred_field']}")
        output(f"GT field:        {m['gt_field']}")
        output("Predicted text:")
        output(m["pred_text"])
        output("GT text:")
        output(m["gt_text"])

    output("\n--- EXTRA / UNMATCHED PREDICTIONS ---")

    for extra in result["extra"]:
        output("-" * 80)
        output(f"Similarity:      {extra['similarity']}")
        output(f"Predicted field: {extra['pred_field']}")
        output("Predicted text:")
        output(extra["pred_text"])

    output("\n--- MISSING GT PARAGRAPHS ---")

    for missing in result["missing"]:
        output("-" * 80)
        output(f"GT field: {missing['field']}")
        output("GT text:")
        output(missing["text"])

    output("\n--- FIELD METRICS ---")

    output(
        f"{'Field':50} "
        f"{'TP':>5} "
        f"{'FP':>5} "
        f"{'FN':>5} "
        f"{'Prec':>8} "
        f"{'Recall':>8} "
        f"{'F1':>8}"
    )

    for field, values in metrics["field_metrics"].items():
        output(
            f"{field:50} "
            f"{values['tp']:5} "
            f"{values['fp']:5} "
            f"{values['fn']:5} "
            f"{values['precision']:8.2%} "
            f"{values['recall']:8.2%} "
            f"{values['f1']:8.2%}"
        )
        

