import { useEffect, useState, useMemo, type FC, type MouseEventHandler, useRef } from 'react'

import type { Recorder } from '../models'

import { useClassName } from '../hooks/className'

export const RecorderComp: FC<Recorder> = (props) => {
  const {
    audioConstraints = true,
    videoConstraints = false,
    peerIdentity,
    preferCurrentTab,
    options,
    submitUrl,
    saveRecording,
    hideText = false,
    text = 'Start Recording',
    stopText = 'Stop Recording',
    hideImage = false,
    imageUrl,
    stopImageUrl,
    imagePosition = 'left',
    imageWidth = '24px',
    imageHeight = '24px',
    displayStyle = 'standard',
    overrideFieldName = 'recording',
  } = props
  const [recordingSubmitUrl, setRecordingSubmitUrl] = useState(submitUrl)
  const [saveRecordings, setSaveRecordings] = useState(saveRecording)
  const [buttonStartText, setButtonStartText] = useState(text)
  const [buttonStopText, setButtonStopText] = useState(stopText)
  const [buttonTextVisible, setButtonTextVisible] = useState(!hideText)
  const [buttonStartImageUrl, setButtonStartImageUrl] = useState(imageUrl)
  const [buttonStopImageUrl, setButtonStopImageUrl] = useState(stopImageUrl ?? imageUrl)
  const [buttonImageVisible, setButtonImageVisible] = useState(!hideImage)
  const [buttonImageWidth, setButtonImageWidth] = useState(imageWidth)
  const [buttonImageHeight, setButtonImageHeight] = useState(imageHeight)
  const [buttonDisplayStyle, setButtonDisplayStyle] = useState(displayStyle)
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const [isRecording, setIsRecording] = useState(false)
  const [recordingFieldName, setRecordingFieldName] = useState(overrideFieldName)

  useEffect(() => {
    setRecordingSubmitUrl(submitUrl)
    setSaveRecordings(saveRecording)
    setButtonTextVisible(!hideText)
    setButtonStartText(hideText ? '' : text)
    setButtonStopText(hideText ? '' : stopText)
    setButtonImageVisible(!hideImage)
    setButtonStartImageUrl(hideImage ? '' : imageUrl)
    setButtonStopImageUrl(hideImage ? '' : stopImageUrl ?? imageUrl)
    setButtonImageWidth(imageWidth)
    setButtonImageHeight(imageHeight)
    setButtonDisplayStyle(displayStyle)
    setRecordingFieldName(overrideFieldName)
  }, [
    submitUrl,
    saveRecording,
    hideText,
    text,
    stopText,
    hideImage,
    imageUrl,
    stopImageUrl,
    imageWidth,
    imageHeight,
    displayStyle,
    overrideFieldName,
  ])

  const handleDownloadRecording = (blob: Blob): void => {
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.style.display = 'none'
    a.href = url
    a.download = 'recording.webm'
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
  }

  const mediaStreamConstraints: MediaStreamConstraints = useMemo(
    () => ({
      audio: audioConstraints ?? true,
      video: videoConstraints ?? false,
      peerIdentity,
      preferCurrentTab,
    }),
    [audioConstraints, videoConstraints, peerIdentity, preferCurrentTab],
  )

  useEffect(() => {
    mediaRecorderRef.current = mediaRecorder
  }, [mediaRecorder])

  useEffect(() => {
    // initialize media recording
    const initMediaRecorder = async (): Promise<void> => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia(mediaStreamConstraints)
        const recorder = new MediaRecorder(stream, options)

        // get recorded data
        recorder.ondataavailable = async (event) => {
          if (event.data.size > 0) {
            const blobRecording = new Blob([event.data], { type: event.data.type })

            if (saveRecordings) {
              console.log('Saving recording')
              handleDownloadRecording(blobRecording)
            }
            if (recordingSubmitUrl) {
              const formData = new FormData()
              formData.append(recordingFieldName, blobRecording)
              const response = await fetch(recordingSubmitUrl, {
                method: 'POST',
                body: formData,
              })
              return response
            }
          }
        }
        setMediaRecorder(recorder)
      } catch (error) {
        console.error('Error initializing media recorder', error)
      }
    }

    initMediaRecorder()

    return () => mediaRecorderRef.current?.stream?.getTracks?.()?.forEach((track) => track.stop())
  }, [options, saveRecordings, recordingFieldName, recordingSubmitUrl, mediaStreamConstraints])

  const handleStartRecording = (): void => {
    if (!mediaRecorder) {
      console.error('Media recorder not initialized')
      return
    }
    setIsRecording(true)
    mediaRecorder.start()
    console.log('Recording started')
  }

  const handleStopRecording = (): void => {
    if (!mediaRecorder) {
      console.error('Media recorder not initialized')
      return
    }
    mediaRecorder.stop()
    setIsRecording(false)
    console.log('Recording stopped')
  }

  const handleOnClick: MouseEventHandler<HTMLButtonElement> = (e) => {
    e.preventDefault()
    isRecording ? handleStopRecording() : handleStartRecording()
  }

  const ImageButton: FC<{
    text?: string
    imageUrl?: string
    disabled?: boolean
  }> = ({ text, imageUrl, disabled = false }) => {
    const leftImgClassName = useClassName(props, { el: 'left-image' })
    const rightImgClassName = useClassName(props, { el: 'right-image' })
    const imgClassName = imagePosition === 'left' ? leftImgClassName : rightImgClassName

    return (
      <button
        className={useClassName(props)}
        onClick={handleOnClick}
        disabled={disabled}
        aria-label={text}
        aria-disabled={disabled}
      >
        {buttonImageVisible && imageUrl && (
          <img
            className={imgClassName}
            src={imageUrl}
            alt={`${text}${disabled ? ' disabled' : ''} button image`}
            style={{
              width: buttonImageWidth,
              height: buttonImageHeight,
            }}
          />
        )}
        {buttonTextVisible && text}
      </button>
    )
  }

  const StandardButtons: FC = (): JSX.Element => (
    <>
      <ImageButton text={buttonStartText} imageUrl={buttonStartImageUrl} disabled={isRecording} />
      <ImageButton text={buttonStopText} imageUrl={buttonStopImageUrl} disabled={!isRecording} />
    </>
  )

  const ToggleButton: FC = (): JSX.Element => {
    const displayText = () => (isRecording ? buttonStopText : buttonStartText)
    const displayImageUrl = () => (isRecording ? buttonStopImageUrl : buttonStartImageUrl)
    return <ImageButton text={displayText()} imageUrl={displayImageUrl()} />
  }

  return (
    <div className={useClassName(props, { el: 'container' })}>
      {buttonDisplayStyle === 'toggle' ? <ToggleButton /> : <StandardButtons />}
    </div>
  )
}
