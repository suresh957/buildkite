echo "buildkite checkout path is $BUILDKITE_BUILD_CHECKOUT_PATH"
cd $BUILDKITE_BUILD_CHECKOUT_PATH
ls
CART_LINK=$(buildkite-agent meta-data get cartlink)
DEVICE=$(buildkite-agent meta-data get device)

echo "Details below!"
echo $CART_LINK
echo $DEVICE
