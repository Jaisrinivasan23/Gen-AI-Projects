import google.generativeai as genai

genai.configure(api_key="AIzaSyC28fVBwe3qhRnluIT4x2mLhElSqexQUC8")

models = genai.list_models()
for model in models:
    print(model.name, "-", model.supported_generation_methods)
