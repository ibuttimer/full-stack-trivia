import React, { useState, useEffect } from "react";
import Button from 'react-bootstrap/Button'
import Col from 'react-bootstrap/Col'
import { useAppContext } from "../libs/contextLib";
import Guess from "./Guess";
import AppIcon from './AppIcon';
import $ from 'jquery';

import '../stylesheets/QuizView.css';

const questionsPerPlay = 5; 

function QuizView () {

    const { user, setUser } = useAppContext();

    const [quizCategory, setQuizCategory] = useState(null);
    const [previousQuestions, setPreviousQuestions] = useState([]);
    const [showAnswer, setShowAnswer] = useState(false);
    const [categories, setCategories] = useState({});
    const [numCorrect, setNumCorrect] = useState(0);
    const [guessCorrect, setGuessCorrect] = useState(false);
    const [numQuestions, setNumQuestions] = useState(0);
    const [currentQuestion, setCurrentQuestion] = useState({});
    const [forceEnd, setForceEnd] = useState(false);


    useEffect(() => {
        $.ajax({
          url: `/api/categories?pagination=n&type=map`,
          type: "GET",
          success: (result) => {
            setCategories(result.categories)
            return;
          },
          error: (error) => {
            alert('Unable to load categories. Please try your request again')
            return;
          }
        })
    }, []); // https://www.robinwieruch.de/react-useeffect-hook mount


    function selectCategory({type, id=0}) {
        let category = {type:type, id:id}
        setQuizCategory(category);
        getNextQuestion(category);
    }


    function getNextQuestion(category) {

        let end = (numQuestions === questionsPerPlay);
        if (!end) {
            const prevQuestions = [...previousQuestions]
            if (currentQuestion.id) {
                prevQuestions.push(currentQuestion.id)
            }
            if (!category) {
                category = quizCategory;
            }
            let requestData = {previous_questions: prevQuestions};
            if (category.id > 0) {
                requestData.quiz_category = category;
            }
            setGuessCorrect(false);

            $.ajax({
                url: '/api/quizzes',
                type: "POST",
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(requestData),
                xhrFields: {
                    withCredentials: true
                },
                crossDomain: true,
                success: (result) => {
                    setShowAnswer(false);
                    setPreviousQuestions(prevQuestions);
                    setCurrentQuestion(result.question);
                    if (result.question) {
                        setForceEnd(false);
                        setNumQuestions(numQuestions + 1);
                    } else {
                        setForceEnd(true);
                    }
                    return;
                },
                error: (error) => {
                    alert('Unable to load question. Please try your request again')
                    return;
                }
            })
        } else {
            setForceEnd(true);
        }
    }


    function submitResults() {
        $.ajax({
            url: '/api/quizzes/results',
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                user_id: user.id,
                num_correct: numCorrect,
                num_questions: numQuestions
            }),
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true,
            success: (result) => {
                setUser(result.user);
                return;
            },
            error: (error) => {
                alert('Unable to save result.')
                return;
            }
        })
    }


    function submitGuess(guess) {
        const evaluation = evaluateAnswer(guess);
        if (evaluation) {
            setNumCorrect(numCorrect + 1);
        }
        setGuessCorrect(evaluation);
        setShowAnswer(true)
    }


    function restartGame() {
        setQuizCategory(null);
        setPreviousQuestions([]);
        setShowAnswer(false);
        setNumCorrect(0);
        setNumQuestions(0);
        setCurrentQuestion({});
        setForceEnd(false);
    }


    function renderPrePlay() {
      return (
          <div className="quiz-play-holder">
              <div className="choose-header">Choose Category</div>
              <div className="category-holder">
                  <div className="play-category" onClick={() => selectCategory({type:'any'})}>ALL</div>
                  {Object.keys(categories).map(id => {
                  return (
                    <div key={id}
                        value={id}
                        className="play-category"
                        onClick={() => selectCategory({type:categories[id], id})}>
                      {categories[id]}
                    </div>
                  )
                })}
              </div>
          </div>
      )
  }


    function renderFinalScore() {
        return(
            <div className="quiz-play-holder">
                <div className="final-header"> Your Final Score is {numCorrect}</div>
                <Col sm={{ span: 10, offset: 5 }}>
                    <Button block size="sm" className="warning col-sm-2" onClick={submitResults}>
                        Save Results
                    </Button>
                    <Button block size="sm" className="col-sm-2" onClick={restartGame}>
                        Play Again?
                    </Button>
                </Col>
            </div>
        )
    }


    function evaluateAnswer(guess) {
        const formatGuess = guess.replace(/[.,/#!$%^&*;:{}=\-_`~()]/g,"").toLowerCase()
        const answerArray = currentQuestion.match.toLowerCase().split(' ');
        return answerArray.every(el => formatGuess.includes(el));
    }


    function renderCorrectAnswer() {
      return(
        <div className="quiz-play-holder">
          <AppIcon sel_icon={quizCategory.type} fontSize="1.5em"/>
          <p>Question {numQuestions} of {questionsPerPlay}</p>
          <div className="quiz-question">{currentQuestion.question}</div>
          <div className={`${guessCorrect ? 'correct' : 'wrong'}`}>{guessCorrect ? "You were correct!" : "You were incorrect"}</div>
          <div className="quiz-answer">{currentQuestion.answer}</div>
          <Col sm={{ span: 10, offset: 5 }}>
              <Button block size="sm" className="col-sm-2" onClick={() => getNextQuestion()}>
                  {(numQuestions === questionsPerPlay) ? "Finish" : "Next Question"}
              </Button>
          </Col>
        </div>
      )
    }


    function renderQuestion() {
      return(
            <div className="quiz-play-holder">
              <AppIcon sel_icon={quizCategory.type} fontSize="1.5em"/>
              <p>Question {numQuestions} of {questionsPerPlay}</p>
              <div className="quiz-question">{currentQuestion.question}</div>
              <Guess submitGuess={submitGuess}/>
            </div>
      )
    }


    function renderPlay() {
        return previousQuestions.length === questionsPerPlay || forceEnd
            ? renderFinalScore()
                : showAnswer
                    ? renderCorrectAnswer()
                        : renderQuestion()
    }

    return quizCategory ? renderPlay() : renderPrePlay();
}

export default QuizView;
