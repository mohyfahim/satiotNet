import os

MYUTILS_PATH = os.path.dirname(os.path.realpath(__file__))

OUTPUT_PATH = os.path.join(MYUTILS_PATH, "../../out")

print(MYUTILS_PATH)
print(OUTPUT_PATH)

if not os.path.isdir(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
