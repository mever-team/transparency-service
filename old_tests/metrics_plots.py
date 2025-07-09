# This example shows how to create a bar plot and put it in the Model Card
import modelcard
import numpy as np

mc = modelcard.model_card_generator.ModelCard()

# Generate fake data
y_true_all = [
    [0, 1, 1, 0, 1, 0],  # data set 1
    [1, 0, 1, 0, 1, 0],  # data set 2
    [0, 1, 0, 0, 1, 0],  # data set 3
    [0, 1, 1, 1, 1, 0],
]  # data set 4
y_pred_model = [
    [0.2, 0.8, 0.6, 0.4, 0.9, 0.1],
    [0.2, 0.9, 0.6, 0.4, 0.2, 0.2],
    [0.1, 0.8, 0.6, 0.5, 0.9, 0.1],
    [0.2, 0.8, 0.7, 0.4, 0.9, 0.9],
]


# Generate AP and ACC data
for i, y_true in enumerate(y_true_all):
    mc.generate_ap_data(y_true, y_pred_model[i], label=f"{i}")
    y_pred = np.array(y_pred_model[i])
    y_pred = y_pred > 0.5
    mc.generate_acc_data(y_true, y_pred, label=f"{i}")

# Initialize bar plots
mc.init_bar_plot(title="ACC data", ylabel="ACC (%)")
mc.init_bar_plot(title="AP data", ylabel="AP (%)")

# Fill the plots with data
mc.fill_bar_plot(
    plot_title="ACC data",
    labels=mc.data["label"].tolist(),
    values=mc.data["acc"].tolist(),
)
mc.fill_bar_plot(
    plot_title="AP data",
    labels=mc.data["label"].tolist(),
    values=mc.data["ap"].tolist(),
)

# Show the plot
mc.show_plot("ACC data")
mc.show_plot("AP data")

# add the plots to the json strucure
mc.add_plot_to(title="ACC data", destination="Eval Set")
mc.add_plot_to(title="AP data", destination="Eval Set")

# Convert to markdown and to html
# mc.save()
