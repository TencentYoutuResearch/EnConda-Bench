# SDG Translations

<a href="https://hosted.weblate.org/engage/sdg-translations/">
<img src="https://hosted.weblate.org/widgets/sdg-translations/-/open-graph.png" alt="Translation status" />
</a>

A project to compile and translate text related to the United Nation's
  Sustainable Development Goals, and then provide those translations as JSON.



These translations are intended primarily for the open-source national reporting platform [Open SDG](https://github.com/open-sdg/open-sdg), but can certainly be used for other NRPs or SDG-related projects.

More information [here](https://open-sdg.org/sdg-translations/).

## Getting started

To use this project locally to generate the JSON files, follow these steps:

1. Clone the repository:
   ```shell
   git clone https://github.com/open-sdg/sdg-translations.git


   ```

2. Create and activate a virtual environment:
   ```shell
   python3 -m venv venv
   venv/bin/activate
   ```



   ```shell
   pip install -r requirements.txt
   python3 -m venv venv


   source venv/bin/activate
   ```

3. Run the build script:

   ```shell
   pip install -r requirements/core.txt


   ```

4. Run the build script:

   ```shell
   python scripts/build_json.py
   ```

4. Install the dependencies:
   ```shell
   pip install requirements.txt
   ```
