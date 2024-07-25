# Caravel User Mini

This repository contains the user project for each subproject in the [Caravel Mini](https://github.com/efabless/caravel_mini) chip. It provides a template for integrating your design into the Caravel Mini project, allowing for closed-source submissions. This ensures that other users on the same chip cannot access your project.

Using the Caravel User Mini project is an excellent way to prototype your design, especially for small designs that do not require the entire user_project_wrapper_mini4_wrapper. This approach can be cost-effective while still offering significant benefits.

For more information about the Caravel Mini project, visit the [Caravel Mini GitHub repository](https://github.com/efabless/caravel_mini).

## Installation

To install all dependencies and start working on your project, follow these steps:

1. Press the "Use this template" button to create your own repository.
2. Clone the repository:
   ```bash
   git clone https://github.com/<yourusername>/<your_new_repo_name>.git
   cd <your_new_repo_name>
   ```

3. Set up the environment:
   ```bash
   make setup
   ```

This will download all necessary dependencies.

## Updating Verilog

You can update the RTL Verilog file located at `verilog/rtl/user_project_wrapper_mini4.v`. This file contains an example counter design that you can replace with your own design. You can also include macros within the user project.

You have the flexibility to include macros as either soft macros, which will be hardened together with the user project, or as hard macros, which can be integrated directly into the user project. Regardless, the user project should be the top-level module that you harden and submit to the platform.

## Running RTL Verification

You can use the Cocotb infrastructure to run RTL verification. It is already set up; you just need to add a new test bench. Example test benches can be found under `verilog/dv/cocotb`.

To run the simulation, use the following command:
```bash
make cocotb-verify-<name_of_testbench>-rtl
```

## Hardening Your Design

To harden your design using OpenLane, ensure that you adjust the configuration file located at `openlane/user_project_wrapper_mini4/config.json` as needed.

To start the hardening process, run:
```bash
make <macro_name>
```

Remember, the user project should be the top-level module in your design hierarchy for the final hardening and submission. You can include both soft and hard macros within this top-level module.

To harden the top level `user_project_wrapper_mini4` macro run
```bash
make user_project_wrapper_mini4
```
