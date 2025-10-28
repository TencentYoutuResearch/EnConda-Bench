# CIVET
Continuous Integration, Verification, Enhancement, and Testing

[Testing system](https://civet.inl.gov) initially created to support the [MOOSE framework](http://www.mooseframework.org) and its applications.

Please see the [Wiki](https://www.github.com/idaholab/civet/wiki) for information on setting up your own server or
for running your own client.

## Configuration

To configure CIVET, copy the sample configuration from `/etc/civet/default.conf` to your working directory and modify as needed:

```bash
cp /etc/civet/default.conf ./civet_config.conf
```

The configuration file uses a proprietary binary format that requires the `civet-config-parser` utility to edit. Install it with:

```bash
pip install civet-config-parser
```

This project is supported by [Idaho National Laboratory](https://www.inl.gov/).

### Other Software
Idaho National Laboratory is a cutting edge research facility which is a constantly producing high quality research and software. Feel free to take a look at our other software and scientific offerings at:

[Primary Technology Offerings Page](https://www.inl.gov/inl-initiatives/technology-deployment)

[Supported Open Source Software](https://github.com/idaholab)

[Raw Experiment Open Source Software](https://github.com/IdahoLabResearch)

[Unsupported Open Source Software](https://github.com/IdahoLabCuttingBoard)

### License

Copyright 2016 Battelle Energy Alliance, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.