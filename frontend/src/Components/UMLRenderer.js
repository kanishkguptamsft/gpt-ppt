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

  useEffect(() => {
    console.log(props.payload);
    setImageUrl(props.payload);
    // fetch('https://dog.ceo/api/breeds/image/random')
    //   .then((res) => res.json())
    //   .then((data) => {
    //     setImageUrl('https://testingaci.blob.core.windows.net/hackchat/ndjljodxvk.png?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-01-25T02%3A57%3A58Z&st=2023-09-13T18%3A57%3A58Z&spr=https&sig=66XZYbaPFUROK4CI%2BAWP1%2BRghH%2BsfQKawjlnLoiZS98%3D');
    //   });
  }, []);

  return (
    <div>
      <TransformWrapper>
      <Controls />
      <TransformComponent>
        {/* need to just pass the url of the image obtained */}
        <img
          src={imageUrl}
          alt="test"
          width="100%"
          height="100%"
        />
      </TransformComponent>
    </TransformWrapper>
    <DownloadIcon/>
    </div>
  );
};

export default UMLRenderer;