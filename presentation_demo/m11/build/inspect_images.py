from zipfile import ZipFile
from pathlib import Path
from PIL import Image
import xml.etree.ElementTree as E
p=Path('presentation_demo/m11');ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with ZipFile(p/'M11_PRESENTASI_TEKNIS_GEDANGAN.pptx') as z:
 for i in [1,3,4,12]:
  s=E.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
  print(i,[(E.tostring(x.find('p:spPr/a:xfrm',ns),encoding='unicode')) for x in s.findall('.//p:pic',ns)])
print('image original',Image.open(p/'assets/02_aerial.png').size)
