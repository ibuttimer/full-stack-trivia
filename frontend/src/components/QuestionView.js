import React, { useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import ListGroup from "react-bootstrap/ListGroup";
import Pagination from 'react-bootstrap/Pagination'

import { useAppContext } from "../libs/contextLib";
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import AppIcon from './AppIcon';
import $ from 'jquery';

function QuestionView () {

    const [response, setResponse] = useState({
        questions: [],
        page: 1,
        perPage: 1,
        totalQuestions: 0,
        categories: {},
        currentCategory: null
    });
    const [request, setRequest] = useState({
        questionTitle: "Questions",
        requestUrl: "",
        requestType: "",
        requestData: null
    });


    useEffect(() => {
        getQuestions();
    }, []); // https://www.robinwieruch.de/react-useeffect-hook mount
    useEffect(() => {}, [response]);


    /* Get questions
     * reqUrl:      url to request
     * reqPage:     results page to request
     * reqType:     request type
     * reqData:     request data
     * reqTitle:    title to display with results
     */
    function requestQuestions(reqUrl, reqPage, reqType, reqData, reqTitle) {
        setRequest({
            questionTitle: reqTitle,
            requestUrl: reqUrl,
            requestType: reqType,
            requestData: reqData
        });

        let request = {
            url: reqUrl + `?page=${reqPage || 1}`,
            type: reqType || "GET",
            success: (result) => {
                storeQuestionsResult(result);
                return;
            },
            error: (error) => {
                alert('Unable to load questions. Please try your request again.')
                return;
            }
        }
        if (reqType === "POST") {
            request.dataType = 'json'
            request.contentType = 'application/json'
            if (reqData) {
                request.data = JSON.stringify(reqData)
            }
            request.xhrFields = {withCredentials: true}
            request.crossDomain = true
        }
        $.ajax(request)
    }

    /* Get page of current questions listing
     * reqPage:     results page to request
     */
    function moreQuestions(reqPage) {
        requestQuestions(request.requestUrl, reqPage, request.requestType, request.requestData, request.questionTitle);
    }


    /* Start all questions listing */
    function getQuestions() {
        requestQuestions(`/api/questions`, null, "GET", null, "Questions");
    }

    const MAX_PG_TABS = 10;
    const MAX_CENTRE_PG_TABS = 5;
    const MAX_SIDE_PG_TABS = Math.floor(MAX_CENTRE_PG_TABS / 2);

    function paginationItem(pageNum) {
        return (<Pagination.Item key={pageNum} active={pageNum === response.page} onClick={() => {moreQuestions(pageNum)}}>
                    {pageNum}
                </Pagination.Item>
          );
    }
    function paginationItems(pageNumbers, start, end) {
          for (let i = start; i <= end; i++) {
             pageNumbers.push(paginationItem(i));
          }
    }
    function createPagination() {
        let pageNumbers = [];
        let maxPage = Math.ceil(response.totalQuestions / response.perPage)
        if (maxPage > MAX_PG_TABS) {
              let firstPage = (response.page === 1);
              let lastPage = (response.page === maxPage);
              pageNumbers.push(
                <Pagination.First key={0} disabled={firstPage} onClick={() => {moreQuestions(1)}}/>
              );
              pageNumbers.push(
                <Pagination.Prev key={-1} disabled={firstPage} onClick={() => {moreQuestions(response.page - 1)}}/>
              );
              let start;
              let end;
              if (response.page <= (MAX_CENTRE_PG_TABS - MAX_SIDE_PG_TABS)) {
                    // << < 1 2 3 4 5 > >>
                    start = 1;
                    end = MAX_CENTRE_PG_TABS;
              } else if (response.page >= (maxPage - MAX_SIDE_PG_TABS)) {
                    // << < 16 17 18 19 20 > >>
                    start = maxPage - MAX_CENTRE_PG_TABS;
                    end = maxPage;
              } else {
                    // << < 2 3 4 5 6 > >>
                    start = response.page - MAX_SIDE_PG_TABS;
                    end = (start + MAX_CENTRE_PG_TABS);
              }
              paginationItems(pageNumbers, start, (end > maxPage ? maxPage : end));
              pageNumbers.push(
                <Pagination.Next key={9999} disabled={lastPage} onClick={() => {moreQuestions(response.page + 1)}}/>
              );
              pageNumbers.push(
                <Pagination.Last key={10000} disabled={lastPage} onClick={() => {moreQuestions(maxPage)}}/>
              );
        } else {
            paginationItems(pageNumbers, 1, maxPage);
        }
        return pageNumbers;
    }


    function storeQuestionsResult(result) {
        setResponse({
                questions: result.questions,
                page: result.page,
                perPage: result.per_page,
                totalQuestions: result.total_questions,
                categories: result.categories,
                currentCategory: result.current_category
            });
    }


    /* Start questions based on category
     * id: category id
     */
    function getByCategory(id) {
        requestQuestions(`/api/categories/${id}/questions`, null, "GET", null, response.categories[id] + " Questions");
    }


    /* Get questions based on a search term.
     * It will return any questions for whom the search term is a substring of the question.
     */
    function submitSearch(searchTerm) {
        requestQuestions(`/api/questions/search`, null, "POST", {searchTerm: searchTerm}, "Search '" + searchTerm + "' Questions");
    }


    function questionAction(id, action) {
        if(action === 'DELETE') {
            $.ajax({
                url: `/api/questions/${id}`,
                type: "DELETE",
                xhrFields: {
                    withCredentials: true
                },
                crossDomain: true,
                success: (result) => {
                    let maxPage = Math.ceil((response.totalQuestions - 1) / response.perPage)
                    let reqPage = (response.page > maxPage ? maxPage : response.page);
                    moreQuestions(reqPage);
                },
                error: (error) => {
                    alert('Unable to delete question. Please try your request again.')
                    return;
                    }
                })
        }
    }

    return (
        <Container fluid>
            <Row>
                <Col xs={2}>
                    <Container>
                        <Row>
                            <Col>
                                <h2 onClick={() => {getQuestions()}}>Categories</h2>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <ListGroup as="ul">
                                    {Object.keys(response.categories).map(id => (
                                      <ListGroup.Item as="li" key={id} active={id == response.currentCategory}
                                                                onClick={() => {getByCategory(id)}}>
                                        <AppIcon sel_icon={response.categories[id]} fontSize="1.5em"/> {response.categories[id]}
                                     </ListGroup.Item>
                                    ))}
                                </ListGroup>
                            </Col>
                        </Row>
                        <Row className="t-margin">
                            <Col>
                                <Search submitSearch={submitSearch}/>
                            </Col>
                        </Row>
                    </Container>
                </Col>
                <Col xs={10}>
                    <Container>
                        <Row>
                            <Col><h2>{request.questionTitle}</h2></Col>
                        </Row>
                        <Row>
                            <Col>
                              {response.questions.map((q, ind) => (
                                <Question
                                  key={q.id}
                                  qid={q.id}
                                  question={q.question}
                                  answer={q.answer}
                                  category={response.categories[q.category]}
                                  difficulty={q.difficulty}
                                  questionAction={questionAction}
                                />
                              ))}
                            </Col>
                        </Row>
                        <Row>
                            <Pagination>{createPagination()}</Pagination>
                        </Row>
                    </Container>
                </Col>
            </Row>
        </Container>
    );
}

export default QuestionView;
