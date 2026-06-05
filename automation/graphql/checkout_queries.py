CHECKOUT_QUERY = """
query Checkout($token: UUID!) {
  checkout(token: $token) {
    id
    token
    lines {
      id
      quantity
      variant {
        id
        name
        sku
      }
    }
  }
}
"""