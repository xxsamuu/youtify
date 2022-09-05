import React, { useContext } from "react";
import { Context } from "../../Context";
import loading from "../../images/loading.svg";
const IsLoading = ({ Page, isLoading }) => {
  const { message } = useContext(Context);
  return (
    <>
      {isLoading ? (
        <div className="loading-wrapper">
          <div className="loading">
            <img src={loading} alt="loading gif" />
            <p>{message}</p>
          </div>
        </div>
      ) : (
        Page
      )}
    </>
  );
};

export default IsLoading;
