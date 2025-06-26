import transparency_service
import sys
import os

sys.path.append(os.path.expanduser("~/rine/src"))
from utils import (
    get_transforms,
    get_our_trained_model,
    get_generators,
)

device = "cuda:0"
generators = get_generators()
_, transform, _ = get_transforms()

mc = transparency_service.model_card_generator.ModelCard()
mc.init_bar_plot(title="rine ACC test", ylabel="ACC (%)")
mc.init_bar_plot(title="rine AP test", ylabel="AP (%)")

# for ncls in [1, 2, 4]:
ncls = 1
# print(f"\n{ncls}-class")
model = get_our_trained_model(ncls=ncls, device=device)

mc.data = transparency_service.evaluation.sid.evaluate(
    model, transform, device=device, tuple_id=0, model_card=mc
)


# mc.save()
