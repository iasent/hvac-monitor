# nodeExporter 셋업

### 설치

```
# raspberry pi 3은 arm7(32bit) 을 사용하므로 해당 arch 전용으로 빌드된 바이너리를 사용해야 한다 
wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-armv7.tar.gz

tar -xvzf node_exporter-1.3.1.linux-armv7.tar.gz

ln -s ./node_exporter-1.3.1.linux-armv7.tar.gz node_exporter
```