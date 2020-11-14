import React, { useState, useEffect } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { Button, Container, Loader } from 'semantic-ui-react';


const Listen = (props: any) => {
    const [showTranscript, setShowTranscript] = useState<boolean>(false);
    useEffect(() => {
        SpeechRecognition.startListening({ continuous: true });
    }, []);
    const commands = [
        {
            command: '*start recording',
            callback: async () => {
                resetTranscript();
                setShowTranscript(true);
            }
        },
        {
            command: '*send message',
            callback: async () => {
                if (showTranscript) {
                    setShowTranscript(false);
                    let finalStr = finalTranscript.replace('send message', '');
                    await props.handleRecording(finalStr);
                    console.log(finalStr);
                    await SpeechRecognition.startListening({ continuous: true });
                    resetTranscript();
                }
            }
        },
        {
            command: '*execute code',
            callback: async () => {
                await props.executeCode();
                console.log('code executed');
                resetTranscript();
            }
        },
        {
            command: '*clear recording',
            callback: async () => {
                resetTranscript();
                console.log('cleared transcript');
            }
        },
        {
            command: '*stop recording',
            callback: async () => {
                setShowTranscript(false);
                resetTranscript();
                console.log('stopped listening');
            }
        }
    ]
    const { transcript, finalTranscript, resetTranscript } = useSpeechRecognition({ commands });

    return (
        <Container>

            <Button color={showTranscript ? 'blue' : undefined} onClick={async () => {
                SpeechRecognition.startListening({ continuous: true });
            }}>
                Record
            </Button>
            <Loader inline active={showTranscript ? true : false} />

            <p>{showTranscript ? transcript : ''}</p>
        </Container >
    )
}

export default Listen