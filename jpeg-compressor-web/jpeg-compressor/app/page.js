'use client'

import NavBar from "@/components/NavBar";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Image from "react-bootstrap/Image";
import Row from "react-bootstrap/Row";
import Form from "react-bootstrap/Form";
import FormGroup from "react-bootstrap/FormGroup";
import Button from "react-bootstrap/Button";

import { useState } from "react";
import { useEffect } from "react";

import server from "@/utils/server";

export default function Home() {

  const [selectedImage, setSelectedImage] = useState();
  const [selectedImageSrc, setSelectedImageSrc] = useState();
  const [compressedImageSrc, setCompressedImageSrc] = useState();
  const [blockSize, setBlockSize] = useState(8)
  const [quantizationScale, setQuantizationScale] = useState(5)
  const [useDefaultMatrix, setUseDefaultMatrix] = useState(true)
  const [downSampleColor, setDownSampleColor] = useState(true)
  const [compressionAlgorithm, setCompressionAlgorithm] = useState(0)
  const [originalSize, setOriginalSize] = useState("?")
  const [compressedSize, setCompressedSize] = useState("?")
  const [compressionRatio, setCompressionRatio] = useState("??.??")
  const [bCompressDisabled, setbCompressDisabled] = useState(true);
  const [bOptionsDisabled, setbOptionsDisabled] = useState(true);

  const imageChange = (e) => {
    if (e.target.files && e.target.files.length > 0){
      setSelectedImage(e.target.files[0]);
    }
  }

  const updateStats = (reqId) => {
    server.get(`/stats/${reqId}`).then((res) => {
      setOriginalSize(res.data.original_size);
      setCompressedSize(res.data.new_size);
      setCompressionRatio(res.data.ratio);
    })
  }

  const compAlgChange = (ev) => {
    setCompressionAlgorithm(ev.target.value)
  }

  useEffect(() => {
    if (selectedImage){
      setSelectedImageSrc(URL.createObjectURL(new Blob([selectedImage], {type: "image/*"})));
      setOriginalSize(selectedImage.size);
      handleCompress();
      setbCompressDisabled(false);
    }
  }, [selectedImage]);

  useEffect(() => {
    setSelectedImageSrc("http://127.0.0.1:5000/default/original");
    setCompressedImageSrc("http://127.0.0.1:5000/default/compressed");
    updateStats("default");
  }, []);

  useEffect(() => {
    if (bOptionsDisabled){
      setBlockSize(8);
      setQuantizationScale(5);
    }
  }, [bOptionsDisabled]);

  const reloadSrc = (e) => {
    e.target.src = selectedImageSrc;
  }

  const handleMtxChck = (e) => {
    setUseDefaultMatrix(!useDefaultMatrix);
    setbOptionsDisabled(!bOptionsDisabled);
  }

  const handleDSChck = (e) => {
    setDownSampleColor(!downSampleColor);
  }

  const handleCompress = () => {
    let formData = new FormData();

    formData.append('img', selectedImage);
    formData.append('blockSize', blockSize);
    formData.append('quantizationScale', quantizationScale);
    formData.append('compressionAlgorithm', compressionAlgorithm);
    formData.append('useDefaultMatrix', useDefaultMatrix ? '1' : '0')
    formData.append('downSampleColor', downSampleColor ? '1' : '0');

    server.post("/compress", formData, {headers: {'Content-Type' : 'multipart/form-data'}}).then((res) => {
      setCompressedImageSrc(`http://127.0.0.1:5000/image/${res.data}`);
      updateStats(res.data);
    })
  }

  return (
  <>
  <NavBar />
  <Container className="mt-3 h-100 p-2">
    <Row>
        <div className="">
          <div>
          <input
            className="form-control"
            accept="image/*"
            type="file"
            onChange={imageChange}
          />
          </div>
        </div>
    </Row>
    </Container>
  <Container className="mt-3 h-100 p-2 border border-dark rounded">
    <div>
    <Row className="">
      <Col className="">
        <h3 className="d-flex align-items-center justify-content-center">Original</h3>
        <div className="d-flex align-items-center justify-content-center">
          <Image className="img-fluid" src={selectedImageSrc} onError={reloadSrc}/>
        </div>
        <p className="d-flex align-items-center justify-content-center mt-3">Size: {originalSize} bytes</p>
      </Col>
      <Col>
        <h3 className="d-flex align-items-center justify-content-center">Compressed</h3>
        <div className="d-flex align-items-center justify-content-center">
          <Image className="img-fluid" src={compressedImageSrc}/>
        </div>
        <p className="d-flex align-items-center justify-content-center mt-3">Size: {compressedSize} bytes ({compressionRatio}% Size Reduction)</p>
      </Col>
    </Row>
    </div>
  </Container>
  <Container className="mt-5">
    <h3>Compression Options</h3>
    <Row>
      <div className="d-flex mt-3 mb-5">
      <Form>
        <FormGroup>
          <Row>
            <Col>
              <Form.Label>Block Size</Form.Label>
              <Form.Control disabled={bOptionsDisabled} size="sm" type="number" value={blockSize} onChange={ (ev) => {
                setBlockSize(ev.target.value)
              }} />
            </Col>
            <Col>
            <Form.Label>Quantization Scale</Form.Label>
            <Form.Control disabled={bOptionsDisabled} size="sm" type="number" value={quantizationScale} onChange={ (ev) => {
              setQuantizationScale(ev.target.value)
            }}/>
            </Col>
          </Row>
        </FormGroup>
        <FormGroup className="mt-3">
            <Form.Label>Compression Algorithm</Form.Label>
              <Form.Select size="sm" onChange={compAlgChange}>
                <option value="0">ZIP</option>
                <option value="1">RLE</option>
              </Form.Select>
        </FormGroup>
        <FormGroup className="mt-3">
            <Form.Check size="sm" defaultChecked={downSampleColor} onChange={handleDSChck} type="checkbox" label="Downsample Colors" id="downSampleColor"/>
            <Form.Check size="sm" defaultChecked={useDefaultMatrix} onChange={handleMtxChck} type="checkbox" label="Use Default Quantization Matrix" id="useDefaultMatrix" />
        </FormGroup>
        <FormGroup className="mt-2 ">
          <Button size="sm" variant="dark" onClick={handleCompress} disabled={bCompressDisabled}>Compress</Button>
          <a href={compressedImageSrc} download="Compressed Image" target='_blank'>
            <Button size="sm" className="m-2" variant="secondary">Download Compressed</Button>
          </a>
        </FormGroup>
        </Form>
      </div>
    </Row>
  </Container>
  </>
  );
}