echo "buildkite checkout path is $BUILDKITE_BUILD_CHECKOUT_PATH"
cd $BUILDKITE_BUILD_CHECKOUT_PATH/.buildkite
ls -a
chmod 755 device.sh build.sh

CART_LINK=$(buildkite-agent meta-data get cartlink)
DEVICE=$(buildkite-agent meta-data get device)

echo "Details below!"
echo $CART_LINK
echo $DEVICE
echo $BUILDKITE_AGENT_NAME
sudo cat $BUILDKITE_BUILD_CHECKOUT_PATH/.buildkite/pipeline.yml


