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
sudo sed -i "s/cartlink-1/$CART_LINK/g" /etc/buildkite-agent/buildkite-agent.cfg
git stash
git checkout master
git pull origin master
sudo sed -i "s/cartlink: 1/$CART_LINK/g" $BUILDKITE_BUILD_CHECKOUT_PATH/.buildkite/pipeline.yml
git add $BUILDKITE_BUILD_CHECKOUT_PATH/.buildkite/pipeline.yml
git commit -m "msg"
git push origin master

