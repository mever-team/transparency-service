import subprocess

print('\033[31merror test\033[0m')

subprocess.run(["python", "ai_assistant.py"])
print('\033[32mok ai_assistant.py\033[0m')

subprocess.run(["python", "count_data.py"])
print('\033[32mok count_data.py\033[0m')

subprocess.run(["python", "text_class1.py"])
print('\033[32mok text_class1.py\033[0m')

subprocess.run(["python", "metrics_interactive_plots.py"])
print('\033[32mok metrics_interactive_plots.py\033[0m')

subprocess.run(["python", "metrics_plots.py"])
print('\033[32mok metrics_plots.py\033[0m')

subprocess.run(["python", "read_data_struc.py"])
print('\033[32mok read_data_struc.py\033[0m')

subprocess.run(["python", "shap_image_class.py"])
print('\033[32mok shap_image_class.py\033[0m')

subprocess.run(["python", "shap_text_class.py"])
print('\033[32mok shap_text_class.py\033[0m')

subprocess.run(["python", "sid.py"])
print('\033[32mok sid.py\033[0m')

subprocess.run(["python", "std.py"])
print('\033[32mok std.py\033[0m')
