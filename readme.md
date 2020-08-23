# Flask-qr-decode

Web application to decode barcodes in images via HTTP. Uses zbar as decoding backend.

## Build

```bash
apt install zbar-tools
pip3 install -r requirements.txt
python3 main.py --host=0.0.0.0 --port=2988
```

Now open http://127.0.0.1:2988/ in your browser, select image file in a form, sibmit it and you'll get scan results as below. Mini images will be shown with rectangles where every barcode was detected in the image.

## Examples

![scan_results1](examples/scan_results1.png)
![scan_results2](examples/scan_results2.png)
