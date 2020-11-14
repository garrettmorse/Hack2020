import React from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { Button, Container } from 'semantic-ui-react';

const Listen = () => {
    const { transcript, resetTranscript } = useSpeechRecognition();
    return (
        <Container>
            <Button onClick={() => SpeechRecognition.startListening()}>Record</Button>
            <Button onClick={SpeechRecognition.stopListening}>Send</Button>
            <Button onClick={resetTranscript}>Clear</Button>
            <p>{transcript}</p>
        </Container>
    )
}

export default Listen