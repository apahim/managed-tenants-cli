# JSON Schema


*managed-tenants-bundles configuration schema for the 'config.yaml' file.*


## Properties


- **`ocm`** *(object)*: Required OCM data for valid imagesets to be constructed by automated MRs to managed-tenants. Cannot contain additional properties.

  - **`addOnParameters`**: List of parameters for the addon. Refer to *shared/addon_parameters.json*.

  - **`addOnRequirements`**: List of requirements for the addon. Refer to *shared/addon_requirements.json*.

  - **`subOperators`**: Sub operator under the umbrella of add-on operator. Refer to *shared/sub_operators.json*.

  - **`subscriptionConfig`**: Subscription config of the addons for the OLM object. Refer to *shared/subscription_config.json*.

- **`addons`** *(array)*: List of addons that use these underlying bundles.

  - **Items** *(object)*: Cannot contain additional properties.

    - **`name`** *(string)*: ID of the addon. (metadata.id).

    - **`environments`** *(array)*: List of all environments in managed-tenants to be upgraded by automated MRs. Production has to be upgraded manually.

      - **Items** *(string)*: Must be one of: `['integration', 'stage']`.
