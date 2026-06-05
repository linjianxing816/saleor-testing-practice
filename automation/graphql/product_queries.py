PRODUCTS_QUERY = """
query Products($channel: String!) {
  products(first: 5, channel: $channel) {
    edges {
      node {
        id
        name
      }
    }
  }
}
"""


PRODUCT_VARIANTS_QUERY = """
query ProductVariants($id: ID!, $channel: String!) {
  product(id: $id, channel: $channel) {
    id
    name
    variants {
      id
      name
      sku
    }
  }
}
"""