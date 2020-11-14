import React, { useState, useEffect } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { Button, Container, Header } from 'semantic-ui-react';
import Siriwave from 'react-siriwave';
import AppRoutes from '../service/app-routes';

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
        },
        {
            command: '*undo',
            callback: async () => {
                await AppRoutes.undoCode()
                    .then(res => {
                        props.onChangeCode(res.data.code);
                    });
            }
        }
    ]
    const { transcript, finalTranscript, resetTranscript } = useSpeechRecognition({ commands });

    return (
        <div>
            <Header as='h3'>Record Speech</Header>

            <Container>
                <Button color={showTranscript ? 'blue' : undefined} onClick={async () => {
                    resetTranscript();
                    setShowTranscript(true);
                }}>
                    Record
            </Button>
                <div style={{ background: 'white' }}>
                    {showTranscript ? (<Siriwave cover={true} amplitude={showTranscript ? 1 : 0.01} style='ios9' />) : null}
                </div>
                <p>{showTranscript ? transcript : ''}</p>
            </Container >
        </div>
    )
}

export default Listen