# Islandora Documentation

[Read the documentation online](https://islandora.github.io/documentation/)

## About this Repository

This "documentation" repository has three functions:

- it **houses the source code for the** [**documentation**](https://islandora.github.io/documentation/) of the [**Islandora project**](https://islandora.ca/) (versions 2.x and above).
- it **hosts the central** [**issue queue**](https://github.com/Islandora/documentation/issues) **for the entire Islandora project**. Add an issue there if you have a use case that isn't addressed, or find a bug.
- its [Wiki](https://github.com/Islandora/documentation/wiki) **contains the archived minutes** for Islandora Tech calls and User calls of previous years. **To find current meeting minutes, please navigate to our** [**community-wiki**](https://github.com/Islandora/islandora-community/wiki).

## Documentation Structure

The documentation is written in [mkdocs](https://www.mkdocs.org/) — the navigation structure is specified in `mkdocs.yml` and the `/docs/` folder contains the content. The text is written in mkdocs-flavoured markdown format and follows our [Documentation Style Guide](https://islandora.github.io/documentation/contributing/docs_style_guide/). Documentation is built and deployed to Github Pages automatically when new commits are added to the 'main' branch.

To build the documentation locally, first install mkdocs version 2.1.0 and then run `mkdocs build` before setting up the virtual environment.




* [Islandora Documentation via Github Pages](https://islandora.github.io/documentation/)

## Local Development

To work on the documentation locally, you first need to install the dependencies.



```bash
pip install mkdocs


```

Then, run the local development server:



```bash
mkdocs run


```




## Older versions

Documentation for Islandora Legacy (7.x) and previous versions is hosted by LYRASIS on a Confluence wiki.

* [Documentation for Islandora Legacy (7.x) and earlier](https://wiki.lyrasis.org/display/ISLANDORA/)

## Maintainers

* [Documentation Interest Group](https://github.com/islandora-interest-groups/Islandora-Documentation-Interest-Group)

## Contributing

To contribute to the Islandora documentation, create an issue or a pull request. To have a pull request accepted, you need to be covered by an Islandora Foundation [Contributor License Agreement](https://github.com/Islandora/islandora-community/wiki/Onboarding-Checklist#contributor-license-agreements) or [Corporate Contributor License Agreement](https://github.com/Islandora/islandora-community/wiki/Onboarding-Checklist#contributor-license-agreements). Please see the [Community](https://www.islandora.ca/community) pages on Islandora.ca for more information.

Use the command `mkdocs server --host 0.0.0.0` to start the local development server.
