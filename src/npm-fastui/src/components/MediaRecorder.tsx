import { useEffect, useState, type FC } from 'react';

export interface MediaRecorderCompProps {
  audioConstraints?: MediaStreamConstraints['audio'];
  videoConstraints?: MediaStreamConstraints['video'];
  peerIdentity?: string;
  preferCurrentTab?: boolean;
  options?: MediaRecorderOptions;
  onRecordingStart?: () => void;
  onRecordingComplete: (blob: Blob) => void;
  hideText?: boolean;
  startText?: string;
  stopText?: string;
  hideImage?: boolean;
  startImageUrl?: string;
  stopImageUrl?: string;
  imagePosition?: 'left' | 'right';
  displayStyle?: 'standard' | 'toggle';
}


export const MediaRecorderComp: FC<MediaRecorderCompProps> = ({
  audioConstraints = true,
  videoConstraints = false,
  peerIdentity,
  preferCurrentTab,
  options,
  onRecordingStart,
  onRecordingComplete,
  hideText = false,
  startText = 'Start Recording',
  stopText = 'Stop Recording',
  hideImage = false,
  startImageUrl,
  stopImageUrl,
  imagePosition = 'left',
  displayStyle = 'standard',
}) => {
  const [buttonStartText, setButtonStartText] = useState(startText);
  const [buttonStopText, setButtonStopText] = useState(stopText);
  const [buttonTextVisible, setButtonTextVisible] = useState(!hideText);
  const [buttonStartImageUrl, setButtonStartImageUrl] = useState(startImageUrl);
  const [buttonStopImageUrl, setButtonStopImageUrl] = useState(stopImageUrl);
  const [buttonImageVisible, setButtonImageVisible] = useState(!hideImage);
  const [buttonDisplayStyle, setButtonDisplayStyle] = useState(displayStyle);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [isRecording, setIsRecording] = useState(false);

  useEffect(() => {
    setButtonTextVisible(!hideText);
    setButtonStartText(hideText ? '' : startText);
    setButtonStopText(hideText ? '' : stopText);
    setButtonStartImageUrl(hideImage ? '' : startImageUrl);
    setButtonStopImageUrl(hideImage ? '' : stopImageUrl);
    setButtonImageVisible(!hideImage);
    setButtonDisplayStyle(displayStyle);
  }, [startText, stopText, hideText, startImageUrl, stopImageUrl, hideImage, displayStyle]);

  useEffect(() => {
    // initialize media recording
    const initMediaRecorder = async () => {
      try {
        const constraints: MediaStreamConstraints = {
          audio: audioConstraints ?? true,
          video: videoConstraints ?? false,
          peerIdentity,
          preferCurrentTab,
        }
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        const recorder = new MediaRecorder(stream, options);
        setMediaRecorder(recorder);
      } catch (error) {
        console.error('Error initializing media recorder', error);
      }
    };

    initMediaRecorder();

    return () => mediaRecorder?.stream?.getTracks?.()?.forEach(track => track.stop());
  }, [audioConstraints, videoConstraints, peerIdentity, preferCurrentTab, options]);

  const handleStartRecording = () => {
    if (!mediaRecorder) {
      console.error('Media recorder not initialized');
      return;
    }
    onRecordingStart?.();
    mediaRecorder.start();
    setIsRecording(true);
    console.log('Recording started');
  }

  const handleStopRecording = () => {
    if (!mediaRecorder) {
      console.error('Media recorder not initialized');
      return;
    }
    mediaRecorder.stop();
    setIsRecording(false);
    console.log('Recording stopped');

    // get recorded data
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        onRecordingComplete(event.data);
      }
    }
  };

  const handleOnClick = () => isRecording ? handleStopRecording() : handleStartRecording();
  const displayText = () => isRecording ? buttonStopText : buttonStartText;
  const displayImageUrl = () => isRecording ? buttonStopImageUrl : buttonStartImageUrl;

  const renderButton = (text?: string, imageUrl?: string, disabled = false) => (
    <button onClick={handleOnClick} disabled={disabled}>
      {buttonImageVisible && imageUrl && (
        <img src={imageUrl} alt="" style={{
          marginRight: imagePosition === 'right' ? '0.5rem' : '0',
          marginLeft: imagePosition === 'left' ? '0.5rem' : '0',
          verticalAlign: 'middle',
        }} />
      )}
      {buttonTextVisible && text}
    </button>
  );

  const renderStandardButtons = () => (
    <>
      {renderButton(buttonStartText, buttonStartImageUrl, isRecording)}
      {renderButton(buttonStopText, buttonStopImageUrl, !isRecording)}
    </>
  );

  return (
    <>
      {buttonDisplayStyle === 'standard' && renderStandardButtons()}
      {buttonDisplayStyle === 'toggle' && renderButton(displayText(), displayImageUrl())}
    </>
  );
}

