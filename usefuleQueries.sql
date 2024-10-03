UPDATE `customer_relations`.`sms`
SET
`status` = 'ready'
WHERE `idSMS` > 0;
UPDATE customer_relations.sms
SET senddate = CASE
    WHEN idSMS = 10 THEN '2024-09-29'  -- 3 days ago (from Oct 2, 2024)
    WHEN idSMS = 9  THEN '2024-09-22'  -- 1 week before
    WHEN idSMS = 8  THEN '2024-09-15'  -- 1 week before
    WHEN idSMS = 7  THEN '2024-09-08'  -- 1 week before
    WHEN idSMS = 6  THEN '2024-09-01'  -- 1 week before
    WHEN idSMS = 5  THEN '2024-08-25'  -- 1 week before
    WHEN idSMS = 4  THEN '2024-08-18'  -- 1 week before
    WHEN idSMS = 3  THEN '2024-08-11'  -- 1 week before
    WHEN idSMS = 2  THEN '2024-08-04'  -- 1 week before
    WHEN idSMS = 1  THEN '2024-07-28'  -- 1 week before
END
WHERE idSMS BETWEEN 1 AND 10;

SELECT 
    c.idCustomers,
    c.Name,
    MAX(s.senddate) AS MostRecentSendDate
FROM 
    customers c
JOIN 
    sms s ON c.idCustomers = s.idcustomer
GROUP BY 
    c.idCustomers, c.Name
ORDER BY 
    MostRecentSendDate DESC;

UPDATE sms
SET senddate = DATE_SUB(senddate, INTERVAL 2 WEEK)
WHERE senddate = '2024-10-02 23:59:38';
