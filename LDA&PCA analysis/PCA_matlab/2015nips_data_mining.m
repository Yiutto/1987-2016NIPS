%%0.First, You must use Matlab to load data
load(2015nips.mat)


%%1. Paper Author Affiliation
T = AcceptedPapers(:,{'Name','Org'});                       % subset table
[T, ~, idx] = unique(T,'rows');                             % remove duplicates
auth = T.(1);                                               % authors
org = cellstr(T.(2));                                       % organizations
w = accumarray(idx, 1);                                     % count of papers
G = digraph(auth,org,w);                                    % create directed graph
G.Nodes.Degree = indegree(G);                               % add indegree
bins = conncomp(G,'OutputForm','cell','Type','weak');       % get connected components
binsizes = cellfun(@length,bins);                           % get bin sizes
small = bins(binsizes < 10);                                % if bin has less than 10
small = unique([small{:}]);                                 % it is small
G = rmnode(G, small);                                       % remove nodes in the bin
org = G.Nodes.Name(ismember(G.Nodes.Name,org));             % get org nodes
deg = G.Nodes.Degree(ismember(G.Nodes.Name,org));           % get org node indegrees
[~, ranking] = sort(deg,'descend');                         % rank by indegrees
topN = org(ranking(1:20));                                  % select top 20
others = org(~ismember(org,topN));                          % select others
markersize = log(G.Nodes.Degree + 2)*3;                     % indeg for marker size
linewidth = 5*G.Edges.Weight/max(G.Edges.Weight);           % weight for line width
figure                                                      % create new figure
h = plot(G,'MarkerSize',markersize,'LineWidth',linewidth,'EdgeAlpha',0.3); % plot graph
highlight(h, topN,'NodeColor',[.85 .33 .1])                 % highlight top 20 nodes
highlight(h, others,'NodeColor',[.93 .69 .13])              % highlight others
labelnode(h,org,org)                                        % label nodes
title({'NIPS 2015 Paper Author Affiliation';'with 10 or more authors'}) % add title


%% 2.Paper Coauthorship
T = AcceptedPapers(:,{'Org','Title'});                      % subset table
[T, ~, idx] = unique(T,'rows');                             % remove duplicates
org = cellstr(T.(1));                                       % organizations
paper = T.(2);                                              % papers
w = accumarray(idx, 1);                                     % count of papers
G = digraph(paper,org,w);                                   % create directed graph
G.Nodes.Degree = indegree(G);                               % add indegree
bins = conncomp(G,'OutputForm','cell','Type','weak');       % get connected components
binsizes = cellfun(@length,bins);                           % get bin sizes
small = bins(binsizes < 5);                                 % if bin has less than 5
small = unique([small{:}]);                                 % it is small
G = rmnode(G, small);                                       % remove nodes in the bin
org = G.Nodes.Name(ismember(G.Nodes.Name,org));             % get org nodes
[~,maxBinIdx] = max(binsizes);                              % index of largest component
topDocs = setdiff(bins{maxBinIdx},org);                     % get docs in largest component
isTopDoc = ismember(AcceptedPapers.Title,topDocs);          % get indices of those docs
topDocIds = unique(AcceptedPapers.PaperID(isTopDoc));       % get the paper ids of those docs
isTopDoc = ismember(Papers.ID,topDocIds);                   % get indices of those docs
markersize = log(G.Nodes.Degree + 2)*3;                     % get org nodes
linewidth = 10*G.Edges.Weight/max(G.Edges.Weight);          % indeg for marker size
figure                                                      % create new figure
h = plot(G,'MarkerSize',markersize,'LineWidth',linewidth,'EdgeAlpha',0.3); % plot graph
highlight(h, topN,'NodeColor',[.85 .33 .1])                 % highlight top 20 nodes
others = org(~ismember(org,topN));                          % select others
highlight(h, others,'NodeColor',[.93 .69 .13])              % highlight others
labelnode(h,topN(1),'Top 20')                               % label nodes
labelnode(h,others([1,4,18,29,72,92,96,99]),'Others')       % label nodes
title({'NIPS 2015 Paper Coauthorship By Affiliation';'with 5 or more nodes'}) % add title


%%3. Paper Topics
Topics = readtable('nips2015_topics.xlsx');                 % load preselected topics
DTM = zeros(height(Papers),height(Topics));                 % document term matrix
for i = 1:height(Topics)                                    % loop over topics
    DTM(:,i) = cellfun(@length, ...                         % get number of matches
        regexpi(Papers.Abstract,Topics.Regex{i}));          % find the word in abstract
end
topDocTopics = sum(DTM(isTopDoc,:));                        % word count in largest component
topDocTopics = topDocTopics ./ sum(topDocTopics) *100;      % convert it into relative percentage
otherDocTopics = sum(DTM(~isTopDoc,:));                     % word count in others
otherDocTopics = otherDocTopics ./ sum(otherDocTopics) *100;% convert it into relative percentage
figure                                                      % create new figure
bar([topDocTopics; otherDocTopics]')                        % bar chart
ax = gca;                                                   % get current axes handle
ax.XTick = 1:height(Topics);                                % set X-axis tick
ax.XTickLabel = Topics.Keyword;                             % set X-axis tick label 
ax.XTickLabelRotation = 90;                                 % rotate X-axis tick label
title('Relative Term Frequency by Document Groups')         % add title
legend('Docs in the Largest Cluster','Other Docs')          % add legend
xlim([0 height(Topics) + 1])                                % set x-axis limits   
ylabel('Percentage')                                        % add y-axis label


%% 4.Topic Grouping by Principal Componet Analysis
w = 1 ./ var(DTM);                                          % inverse variable variances
[wcoeff, score, latent, tsquared, explained] = ...          % weighted PCA with w
    pca(DTM, 'VariableWeights', w);
coefforth = diag(sqrt(w)) * wcoeff;                         % turn wcoeff to orthonormal
labels = Topics.Keyword;                                    % Topics as labels
topT = Topics.Keyword((topDocTopics - otherDocTopics) > 1); % topics popular in top cluster
figure                                                      % new figure
biplot(coefforth(:,1:2), 'Scores', score(:,1:2), ...        % 2D biplot with the first two comps
    'VarLabels', labels)
title('Principal Components Analysis of Paper Topics')      % add title
for i =  1:length(topT)                                     % loop over popular topics
    htext = findobj(gca,'String',topT{i});                  % find text object
    htext.Color = [.85 .33 .1];                             % highlight by color
end
rectangle('Position',[.05 -.1 .5 .3],'Curvature',1, ...     % add rectagle
    'EdgeColor',[0 .5 0])
rectangle('Position',[-.23 .05 .25 .55],'Curvature',1, ...  % add rectangle
    'EdgeColor',[.6 .1 .5])
rectangle('Position',[-.35 -.4 .34 .42],'Curvature',1, ...  % add rectangle
    'EdgeColor',[.1 .2 .6])


%% 5,Deep Learning
axis([-0.1 0.5 -0.1 0.2]);                                  % define axis limits


%%6. Core Algorithms
axis([-0.06 0.06 -0.06 0.06]);                                  % define axis limits


%% 7.Commercial Research
isGoogler = AcceptedPapers.Org == 'Google';                 % find indices of Google authors
GooglePaperIds = unique(AcceptedPapers.PaperID(isGoogler)); % find their paper ids
isGooglePaper = ismember(Papers.ID,GooglePaperIds);         % get the paper indices
GoogleTopics = sum(DTM(isGooglePaper,:));                   % sum Google rows
GoogleTopics = GoogleTopics ./ sum(GoogleTopics) *100;      % convert it into relative percentage
isIBMer = AcceptedPapers.Org == 'IBM';                      % find indices of IBM authors
IBMPaperIds = unique(AcceptedPapers.PaperID(isIBMer));      % find their paper ids
isIBMPaper = ismember(Papers.ID,IBMPaperIds);               % get the paper indices
IBMTopics = sum(DTM(isIBMPaper,:));                         % sum IBM rows
IBMTopics = IBMTopics ./ sum(IBMTopics) *100;               % convert it into relative percentage
isMSofter = AcceptedPapers.Org == 'Microsoft';              % find indices of Mirosoft authors
MSPaperIds = unique(AcceptedPapers.PaperID(isMSofter));     % find their paper ids
isMSPaper = ismember(Papers.ID,MSPaperIds);                 % get the paper indices
MSTopics = sum(DTM(isMSPaper,:));                           % sum Microsoft rows
MSTopics = MSTopics ./ sum(MSTopics) *100;                  % convert it into relative percentage
commercialTopics = [GoogleTopics; IBMTopics; MSTopics];     % combine all
figure                                                      % new figure
biplot(coefforth(:,1:2), 'Scores', score(:,1:2), ...        % 2D biplot with the first two comps
    'VarLabels', labels)
hline = findobj(gca,'LineStyle','none');                    % get line handles of observations
for i = 1:length(hline)                                     % loop over observatoins
    hline(i).Visible = 'off';                               % make it invisible
end
htext = findobj(gca,'Type','text');                         % get text handles
tcolor = [0 .5 0;.85 .33 .1; .1 .2 .6];                     % define text color
for i = 1:length(htext)                                     % loop over text
   r = commercialTopics(:,strcmp(labels,htext(i).String));  % get ratios
   if sum(r) == 0                                           % if all rows are zero
       htext(i).Visible = 'off';                            % make it invisible
   else                                                     % otherwise
       [~,idx] = max(r);                                    % get max row
       htext(i).Color = tcolor(idx,:);                      % use matching color
   end
end
text(-.4,.3,'Google','Color',tcolor(1,:),'FontSize',14)     % annotate
text(.3,-.1,'IBM','Color',tcolor(2,:),'FontSize',14)        % annotate
text(-.4,-.2,'Microsoft','Color',tcolor(3,:),'FontSize',14) % annotate
title({'Principal Components Analysis of Paper Topics';     % add title
    'highlighting Google, IBM and Microsoft topics'}) 

     
%%8. Top 10 Authors in NIPS 2015
[auth_ids,~,idx] = unique(AcceptedPapers.ID);               % get author ids
count = accumarray(idx,1);                                  % get count
[~,ranking] = sort(count,'descend');                        % get ranking
top10_ids = auth_ids(ranking(1:10));                        % get top 10 ids
isTop10 = ismember(AcceptedPapers.ID,top10_ids);            % get row indices
top10_paper_ids = unique(AcceptedPapers.PaperID(isTop10));  % get top 10 papaer ids
isTop10paper = ismember(Papers.ID,top10_paper_ids);         % get row indices
top10Topics = sum(DTM(isTop10paper ,:));                    % sum top 10 rows
top10Topics = top10Topics ./ sum(top10Topics) *100;         % convert it into relative percentage
notTop10Topics = sum(DTM(~top10Topics,:));                  % word count in others
notTop10Topics = notTop10Topics ./ sum(notTop10Topics) *100;% convert it into relative percentage
combined = [top10Topics;notTop10Topics];                    % combine all
[isTop10Author,order] = ismember(Authors.ID,top10_ids);     % get indices of top 10 authors
[~,order] = sort(order(isTop10Author));                     % get ranking
names = Authors.Name(isTop10Author);                        % get names
figure                                                      % create new figure
biplot(coefforth(:,1:2), 'Scores', score(:,1:2), ...        % 2D biplot with the first two comps
    'VarLabels', labels)
hline = findobj(gca,'LineStyle','none');                    % get line handles of observations
for i = 1:length(hline)                                     % loop over observatoins
    hline(i).Visible = 'off';                               % make it invisible
end
htext = findobj(gca,'Type','text');                         % get text handles
tcolor = [.85 .33 .1; .1 .2 .6];                            % define text color
for i = 1:length(htext)                                     % loop over text
   r = combined(:,strcmp(labels,htext(i).String));          % get ratios
   [~,idx] = max(r);                                        % get max row
   if idx == 1 && r(1) > 3                                  % if row 1 & r > 3
       htext(i).Color = [.85 .33 .1];                       % highlight text
   else
        htext(i).Color = [.6 .6 .6];                        % ghost text
   end
end
title({'Principal Components Analysis of Paper Topics';     % add title
    'highlighting topics by top 10 authors'})
text(-.5,.3,'Top 10 ','FontWeight','bold')                  % annotate
text(-.5,0,names(order))                                    % annotate