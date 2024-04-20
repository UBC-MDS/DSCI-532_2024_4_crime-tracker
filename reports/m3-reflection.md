 # Reflection at Milestone 3

 Since Milestone 1, we have made significant progress in developing our Crime Tracker dashboard for Vancouver. Initially we had planed to have a sidebar with a multi-selection dropdown for filtering based on neighbourhood and crime type. However, for Milestone 2 we went through with separating the dropdown to be specific for the plots as some bars should only be affected by one selection filter and not both. Our decision was based upon the reasoning that if the user makes a selection in the filter dropdown but one of the bar charts does not change, it may cause confusion. To resolve this, we changed the layout so that the bar charts are now below the selection filters so that there is more clarity in terms of which plots will change due to which filter selection. This redesign is a mjor update in our dashboard. Plus, another update that has been made to the layout is that the map plot has been made more central as it is the crux of our dashboard.

 In addition to this, we have some more changes that we incorporated that were based off of the feedback provided on our initial version of the dashboard from Milestone 2. Initially, the selection filters only allowed the user to select either a single neighbourhood/crime type or all neighbourhoods/crime types. Along with this, regardless of the neighbourhood or crime type selected, the colour of an individual selection was always static. This has now been updated to provide users with multi-selection, alongside a specific and consistent color mapping. 

 A final overall change that has been made to the dashboard, that was part of our initial plan and part of the first version of the dashboard in Milestone 2, is the removal of the static statistics at the top of the dashboard including: total crime count and the top 3 crime counts.

 Moving forward, we are planning to include background CSS styling in our dashboard to improve the visual aesthetics of the dashboard. Additionally, the data sampling method will also be modified in order to have the regions, with the data points on the map, to be more connected rather than being separated. Currently, the limitation that was faced is that we are able to deploy the dashboard with a limited amount of data. To overcome this, data loading through batches will be explored further.



