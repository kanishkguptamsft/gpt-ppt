import React, { useEffect, useState } from 'react';
import IconButton from '@mui/material/IconButton';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import ZoomOutIcon from '@mui/icons-material/ZoomOut';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import Link from '@mui/material/Link';
import {
    TransformWrapper,
    TransformComponent,
    useControls
  } from "react-zoom-pan-pinch";

const UMLRenderer = (props) => {
  const Controls = () => {
      const { zoomIn, zoomOut, resetTransform } = useControls();
      return (
        <>
          <IconButton onClick={() => zoomIn()}><ZoomInIcon/></IconButton>
          <IconButton onClick={() => zoomOut()}><ZoomOutIcon/></IconButton>
          <IconButton onClick={() => resetTransform()}><RestartAltIcon/></IconButton>
        </>
      );
    };
  const [imageUrl, setImageUrl] = useState('');
  const [documentUrl, setDocumentUrl] = useState('');

  useEffect(() => {
    console.log(props.payload);
    setImageUrl(props.payload['diagram']);
    setDocumentUrl(props.payload['document']);
  }, []);

  return (
    <div>
      <TransformWrapper>
      <Controls />
      <TransformComponent>
        <img
          src={imageUrl}
          alt="test"
          width="100%"
          height="100%"
        />
      </TransformComponent>
    </TransformWrapper>
    <Link target="_blank" href={documentUrl} rel="noreferrer">
    Open design document
    </Link>
    </div>
  );
};

export default UMLRenderer;