// new file called DogPicture.jsx
import React, { useEffect, useState } from 'react';

import IconButton from '@mui/material/IconButton';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import ZoomOutIcon from '@mui/icons-material/ZoomOut';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import DownloadIcon from '@mui/icons-material/Download';

import {
    TransformWrapper,
    TransformComponent,
    useControls
  } from "react-zoom-pan-pinch";

const UMLRenderer = () => {
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

  useEffect(() => {
    fetch('https://dog.ceo/api/breeds/image/random')
      .then((res) => res.json())
      .then((data) => {
        setImageUrl(data.message);
      });
  }, []);

  return (
    <div>
      <TransformWrapper>
      <Controls />
      <TransformComponent>
        {/* need to just pass the url of the image obtained */}
        <img
          src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80"
          alt="test"
          width="50%"
          height="60%"
        />
      </TransformComponent>
    </TransformWrapper>
    <DownloadIcon/>
    </div>
  );
};

export default UMLRenderer;