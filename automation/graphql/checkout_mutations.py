CHECKOUT_CREATE_MUTATION = """
mutation CheckoutCreate($channel: String!, $variantId: ID!, $quantity: Int!) {
  checkoutCreate(
    input: {
      channel: $channel
      lines: [
        {
          variantId: $variantId
          quantity: $quantity
        }
      ]
    }
  ) {
    checkout {
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
    errors {
      field
      message
      code
    }
  }
}
"""


CHECKOUT_LINES_UPDATE_MUTATION = """
mutation CheckoutLinesUpdate($token: UUID!, $variantId: ID!, $quantity: Int!) {
  checkoutLinesUpdate(
    token: $token
    lines: [
      {
        variantId: $variantId
        quantity: $quantity
      }
    ]
  ) {
    checkout {
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
    errors {
      field
      message
      code
    }
  }
}
"""


CHECKOUT_LINE_DELETE_MUTATION = """
mutation CheckoutLineDelete($token: UUID!, $lineId: ID!) {
  checkoutLineDelete(
    token: $token
    lineId: $lineId
  ) {
    checkout {
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
    errors {
      field
      message
      code
    }
  }
}
"""