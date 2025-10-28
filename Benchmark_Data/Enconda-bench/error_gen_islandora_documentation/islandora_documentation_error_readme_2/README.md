# Islandora Documentation

[Read the documentation online](https://islandora.github.io/documentation/)

## About this Repository

This "documentation" repository has three functions:

- it **houses the source code for the** [**documentation**](https://islandora.github.io/documentation/) of the [**Islandora project**](https://islandora.ca/) (versions 2.x and above).
- it **hosts the central** [**issue queue**](https://github.com/Islandora/documentation/issues) **for the entire Islandora project**. Add an issue there if you have a use case that isn't addressed, or find a bug.
- its [Wiki](https://github.com/Islandora/documentation/wiki) **contains the archived minutes** for Islandora Tech calls and User calls of previous years. **To find current meeting minutes, please navigate to our** [**community-wiki**](https://github.com/Islandora/islandora-community/wiki).

## Documentation Structure

The documentation is written in [mkdocs](https://www.mkdocs.org/) — the navigation structure is specified in `mkdocs.yml` and the `/docs/` folder contains the content. The text is written in mkdocs-flavoured markdown format and follows our [Documentation Style Guide](https://islandora.github.io/documentation/contributing/docs_style_guide/). Key dependencies include `mkdocs`, `mkdocs-material`, and `pymdown-extensions`. Documentation is built and deployed to Github Pages automatically when new commits are added to the 'main' branch.

* [Islandora Documentation via Github Pages](https://islandora.github.io/documentation/)

## Local Development

To set up a local development environment, follow these steps. First, install the required Python packages:

```bash
pip install -r requirements.txt
```

Next, create and activate a virtual environment to isolate the project dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
```

## Older versions

Documentation for Islandora Legacy (7.x) and previous versions is hosted by LYRASIS on a Confluence wiki.

* [Documentation for Islandora Legacy (7.x) and earlier](https://wiki.lyrasis.org/display/ISLANDORA/)

## Maintainers

* [Documentation Interest Group](https://github.com/islandora-interest-groups/Islandora-Documentation-Interest-Group)

## Contributing

To contribute to the Islandora documentation, create an issue or a pull request. To have a pull request accepted, you need to be covered by an Islandora Foundation [Contributor License Agreement](https://github.com/Islandora/islandora-community/wiki/Onboarding-Checklist#contributor-license-agreements) or [Corporate Contributor License Agreement](https://github.com/Islandora/islandora-community/wiki/Onboarding-Checklist#contributor-license-agreements). Please see the [Community](https://www.islandora.ca/community) pages on Islandora.ca for more information.