# `/tools`

The tools command group provides various tools for calculating infrastructure,
land, city, project, and resource costs.

## `/tools infrastructure`

Calculates the cost to buy infrastructure from the before
amount to the after amount.

### Parameters

- `before` : {{ $var.toolsBeforeInfrastructureArgument }}
- `after` : {{ $var.toolsAfterInfrastructureArgument }}
- `urbanization_policy` : Whether or not to account for the Urbanization Policy.
  {{ $var.defaultFalseArgument }}
- `center_for_civil_engineering` : Whether or not to account for the Center for
  Civil Engineering Project. {{ $var.defaultFalseArgument }}
- `advanced_engineering_corps` : Whether or not to account for the Advanced
  Engineering Corps Project. {{ $var.defaultFalseArgument }}

## `/tools land`

Calculates the cost to buy land from the before
amount to the after amount.

### Parameters

- `before` : {{ $var.toolsBeforeLandArgument }}
- `after` : {{ $var.toolsAfterLandArgument }}
- `rapid_expansion_policy` : Whether or not to account for the Rapid Expansion
  Policy. {{ $var.defaultFalseArgument }}
- `arable_land_agency` : Whether or not to account for the Arable Land Agency Project.
  {{ $var.defaultFalseArgument }}
- `advanced_engineering_corps` : Whether or not to account for the Advanced
  Engineering Corps Project. {{ $var.defaultFalseArgument }}

## `/tools city`

Calculates the cost to buy cities from the before
amount to the after amount.

### Parameters

- `before` : {{ $var.toolsBeforeCityArgument }}
- `after` : {{ $var.toolsAfterCityArgument }}
- `manifest_destiny_policy` : Whether or not to account for the Manifest Destiny
  Policy. {{ $var.defaultFalseArgument }}
- `urban_planning` : Whether or not to account for the Urban Planning Project.
  {{ $var.defaultFalseArgument }}
- `advanced_urban_planning` : Whether or not to account for the Advanced Urban
  Planning Project. {{ $var.defaultFalseArgument }}

## `/tools projects`

Calculate the cost of buying projects.

### Parameters

- `technological_advancement` : Whether or not to account for the Technological
  Advancement Policy. {{ $var.defaultFalseArgument }}
- `page` : The page of projects to show.

## `/tools calculate-value`

Calculates the value of the provided resources.

### Parameters

- `resources` : {{ $var.resourcesArgument }}

## `/tools nation infrastructure`

Calculates the cost to modify a nation's infrastructure to
the provided amount in each city.

### Parameters

- `after` : {{ $var.toolsAfterInfrastructureArgument }}
- `nation` : {{ $var.nationArgument }}
- `only_buy` : {{ $var.onlyBuyArgument }} {{ $var.defaultFalseArgument }}

## `/tools nation land`

Calculates the cost to modify a nation's land to
the provided amount in each city.

### Parameters

- `after` : {{ $var.toolsAfterLandArgument }}
- `nation` : {{ $var.nationArgument }}
- `only_buy` : {{ $var.onlyBuyArgument }} {{ $var.defaultFalseArgument }}

## `/tools nation city`

Calculates the cost to buy a nation to a specified city count.

- `after` : {{ $var.toolsAfterCityArgument }}
- `nation` : {{ $var.nationArgument }}

## `/tools nation projects`

Calculate the cost of buying projects for a nation.

### Parameters

- `nation` : {{ $var.nationArgument }}
- `page` : The page of projects to show.

## `/tools alliance infrastructure`

Calculates the cost to modify every nation's infrastructure in the provided
alliance to the amount specified in each city.

### Parameters

- `after` : {{ $var.toolsAfterInfrastructureArgument }}
- `alliance` : {{ $var.allianceArgument }}
- `only_buy` : {{ $var.onlyBuyArgument }} {{ $var.defaultFalseArgument }}

## `/tools alliance land`

Calculates the cost to modify every nation's land in the provided
alliance to the amount specified in each city.

### Parameters

- `after` : {{ $var.toolsAfterLandArgument }}
- `alliance` : {{ $var.allianceArgument }}
- `only_buy` : {{ $var.onlyBuyArgument }} {{ $var.defaultFalseArgument }}

## `/tools alliance city`

Calculates the cost to buy every nation in the provided alliance to
a specified city count.

- `after` : {{ $var.toolsAfterCityArgument }}
- `alliance` : {{ $var.allianceArgument }}

## `/tools alliance projects`

Calculate the cost of buying a project for every nation in
the provided alliance.

### Parameters

- `alliance` : {{ $var.allianceArgument }}
- `page` : The page of projects to show.
