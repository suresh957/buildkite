CART_LINK=$(buildkite-agent meta-data get cartlink)
DEVICE=$(buildkite-agent meta-data get device)

echo "Details below!"
echo $CART_LINK
echo $DEVICE
