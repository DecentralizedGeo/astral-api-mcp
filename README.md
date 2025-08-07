# astral-api-mcp

A MCP (Model Context Protocol) server that enables AI models to query location attestations using the available Astral GraphQL endpoints and APIs.

## Project Overview

We are exploring the development of a Model Context Protocol (MCP) agent that integrates with the [Astral API](https://docs.astral.global/getting-started) to enable intelligent querying and analysis of attestations submitted to blockchain ecosystems such as the Ethereum Attestation Service (EAS). This agent would support complex queries across spatial and temporal dimensions, such as filtering attestations by schema ID, location, or date range, while maintaining persistent context across sessions. By leveraging Astral’s structured API and EAS’s open schema model, the agent could automate common analytical workflows—like generating attestation heatmaps or tracking schema usage over time—making it a valuable tool for both research and production use cases. This early scoping phase would help assess feasibility and determine if this direction merits further investment.

To learn more, please refer to the following [document](docs/ai/README.md) for additional details on the purpose, use cases, architecture, and development plans.

## Integration with the Recall Platform

[Recall](https://docs.recall.network/advanced/overview) is a blockchain-based platform to support persistent, intelligent agents for onchain storage primitives and agent collaboration tools, enabling AI agents to maintain persistent memory, share data across sessions, and participate in a broader ecosystem of interconnected agents. By integrating the Astral MCP agent with Recall, we can transform it from a standalone location attestation query tool into a collaborative participant in an agent network with long-term memory—enabling it to store spatial analysis insights onchain, build knowledge graphs of location patterns over time, and share geospatial intelligence with other agents in the ecosystem. This integration unlocks powerful capabilities like persistent session context, cross-agent location verification services, and the ability to contribute to community-driven location intelligence, positioning your agent as both a consumer and provider of valuable spatial data within a growing network of AI agents that can learn from and build upon each other's discoveries.

Once the Astral MCP agent is functional, we plan to integrate it with the Recall platform to enable persistent memory by storing insights onchain. You can find out more details on this next stage of development [in the following section](./docs/integration-with-recall.md).
